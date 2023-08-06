"Hanlder of the services management:  config files templating, service reload..."
import logging
import subprocess
import hashlib
import os
import glob
import time
import shutil
import jinja2
import prometheus_client

cfg_metric = prometheus_client.Enum("lb_config_state_status", "Status of all config file",
                                        ['file', 'name'], states=['valid', 'invalid'])

class DaemonConfig:
    "Daemon config manager"
    def __init__(self, name, config_check, config_file, temp_config_file, template_file, backup_file, backup_file_number):
        self._name = name
        self._config_check = config_check
        self._config_file = config_file
        self._temp_config_file = temp_config_file
        self._template_file = template_file
        self._backup_file = backup_file
        self._backup_file_number = backup_file_number
        self._reload_command = ['sudo', 'systemctl', 'reload-or-restart', self._name]

    def _test_config(self):
        "launch command to parse config file"
        res = subprocess.run(self._config_check)
        return res.returncode == 0

    def _reload_config(self):
        "restart/reloead service"
        res = subprocess.run(self._reload_command)
        return res.returncode == 0

    def _get_previous_config_sha256(self):
        "get current config file fingerprint"
        if not os.path.exists(self._config_file):
            return 'An impossible digest'
        with open(self._config_file, "rb") as f_handle:
            read_bytes = f_handle.read()
            return hashlib.sha256(read_bytes).hexdigest()

    def _templatize_config(self, env, cache, config):
        "regenerate config and return True if file has changed"
        previous_sha256 = self._get_previous_config_sha256()
        tmpl = env.get_template(self._template_file)
        new_content = tmpl.render(svcs=cache.svcs, hosts=cache.nodes, config=config)
        current_sha256 = hashlib.sha256(new_content.encode('utf-8')).hexdigest()
        if current_sha256 == previous_sha256:
            logging.debug('Config %s file for %s unchanged', self._config_file, self._name)
            return False
        logging.debug('Config %s file for %s is different from existing one', self._config_file,
                      self._name)
        with open(self._temp_config_file, 'w') as output_file:
            output_file.write(new_content)
        logging.debug('Config %s file for %s written', self._config_file, self._name)
        return True

    def _rotate_config(self):
        shutil.copy(self._config_file, self._backup_file + '-backup-'+ time.strftime("%Y%m%d-%H%M%S"))
        filelist = sorted(glob.glob(self._backup_file + '-backup-*'), reverse=True)
        logging.debug("File list: %s"%filelist)
        for file_backup in filelist[self._backup_file_number:]:
            os.remove(file_backup)
            logging.info('Delete old %s file for %s', file_backup, self._name)

    def update_config(self, env, cache, config):
        "refresh config"
        logging.debug('Generating config %s file for %s', self._config_file, self._name)
        if self._templatize_config(env, cache, config):
            if self._test_config():
                logging.info('Config file %s for %s is valid, renaming to %s and reloading service',
                             self._temp_config_file, self._name, self._config_file)
                os.rename(self._temp_config_file, self._config_file)
                self._rotate_config()
                cfg_metric.labels(self._config_file, self._name).state('valid')
                if self._reload_config():
                    logging.debug('Reloading service for %s succeeded', self._name)
                else:
                    logging.error('Reloading service for %s failed', self._name)
            else:
                cfg_metric.labels(self._config_file, self._name).state('invalid')
                logging.error('Config file %s for %s is not valid!!', self._config_file,
                              self._name)
        else:
            #return valid if current file is same that precedent
            cfg_metric.labels(self._config_file, self._name).state('valid')


class DaemonController:
    "Class tha wrap all daemon management"
    def __init__(self, cache, config):
        self._cache = cache
        self._daemon_config = []
        for (key, item) in config['daemon_config'].items():
            logging.info('Preparing daemon configuration for %s', key)
            self._daemon_config.append(DaemonConfig(key,
                                                    item['check_command'],
                                                    item['generated_config_file'],
                                                    item['temp_generated_config_file'],
                                                    item['template_file'],
                                                    item['backup_file'],
                                                    item['backup_file_number']))
        self._config = config
        self._env = jinja2.Environment(loader=jinja2.FileSystemLoader(config['templates']))

    @property
    def keep_going(self):
        return True

    def sync_config(self):
        "Ensure all Daemons config files are up2date"
        for daemon in self._daemon_config:
            daemon.update_config(self._env, self._cache, self._config)
