"Da main"

import logging
import sys
import asyncio
import kubernetes_asyncio as kubernetes
import prometheus_client

# local imports
import k8s_cache, daemon, cli_parse, event_handler

async def setup_k8s_connection():
    "Setup K8s connection, in-cluster or not"
    try:
        await kubernetes.config.load_incluster_config()
        logging.info('In-cluster config succeeded')
    except Exception:
        await kubernetes.config.load_kube_config()
        logging.info('KUBECONFIG config succeeded')

def main():
    "Da main"
    config = cli_parse.parse()
    cache = k8s_cache.K8sCache(*config['ip_nets'])
    daemon_controller = daemon.DaemonController(cache, config)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup_k8s_connection())
    logging.info('Operator Ready')
    v1_api = kubernetes.client.CoreV1Api()
    svc_metric = prometheus_client.Enum("lb_svc_sync_status", "Status of all services managed",
                                        ['namespace', 'name'], states=['valid', 'invalid'])
    prometheus_client.start_http_server(config['metrics']['port'], addr=config['metrics']['addr'])

    while True:
        try:
            task1 = loop.create_task(event_handler.watch_services(v1_api, cache, svc_metric))
            task2 = loop.create_task(event_handler.watch_nodes(v1_api, cache))
            task3 = loop.create_task(event_handler.regenerate_config(daemon_controller))
            loop.run_until_complete(asyncio.gather(task1, task2, task3))
        except KeyboardInterrupt:
            logging.info("Stopping")
            sys.exit(0)

if __name__ == '__main__':
    main()
