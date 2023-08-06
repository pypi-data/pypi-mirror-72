"cli and configuration parser utility"

import os
import argparse
import logging
import yaml

_DEF_CONFIG_FILE = '/etc/lb-controller/lb-controller.yaml'
_TEXT_TO_LOG_LEVELS = ['notset', 'debug', 'info', 'warning', 'error', 'critical']

def _read_config(config_file):
    "YAML loader"
    with open(config_file) as stream:
        return yaml.safe_load(stream)

def parse():
    "Parse cli arguments"
    parser = argparse.ArgumentParser(description='External K8s loadbalancer')
    parser.add_argument('-c', '--config', dest='config_filename',
                        default=os.getenv('LB_CONTROLLER_CONFIG', _DEF_CONFIG_FILE),
                        help=f'read configuration from CONFIG (defaults to $LB_CONTROLLER_CONFIG or {_DEF_CONFIG_FILE})',
                        metavar='CONFIG')
    parser.add_argument('-l', '--log-level',
                        dest='log_level', default='info',
                        choices=_TEXT_TO_LOG_LEVELS,
                        metavar='LEVEL',
                        help=f'set log level ({", ".join(list(_TEXT_TO_LOG_LEVELS))})')

    args = parser.parse_args()
    logging.basicConfig(level=args.log_level.upper())
    return _read_config(args.config_filename)
