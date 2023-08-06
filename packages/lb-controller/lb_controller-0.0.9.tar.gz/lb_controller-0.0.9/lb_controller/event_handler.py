"Event Handler and helper functions"
import logging
import asyncio
import aiohttp
import kubernetes_asyncio as kubernetes

update_needed = False
lock = asyncio.Lock()

async def _update_service(v1_api, svc, status, cause=None):
    "Update K8s svc to refect its sync state"
    if status:
        svc = await v1_api.patch_namespaced_service(svc.metadata.name,
                                                    svc.metadata.namespace,
                                                    {'metadata': {'annotations': {
                                                        'external-lb/sync-status': 'valid',
                                                        'external-lb/sync-status-cause': None}}})

        svc.status = kubernetes.client.V1ServiceStatus()
        if svc.spec.type == 'LoadBalancer':
            svc.status.load_balancer=kubernetes.client.V1LoadBalancerStatus(
                ingress=[kubernetes.client.V1LoadBalancerIngress(ip=svc.spec.load_balancer_ip)]
            )
    else:
        svc = await v1_api.patch_namespaced_service(svc.metadata.name,
                                                    svc.metadata.namespace,
                                                    {'metadata': {'annotations': {
                                                        'external-lb/sync-status': 'invalid',
                                                        'external-lb/sync-status-cause': cause}}})
        svc.status = kubernetes.client.V1ServiceStatus()
    return await v1_api.replace_namespaced_service_status(svc.metadata.name,
                                                          svc.metadata.namespace,
                                                          svc)

async def handle_service_event(v1_api, cache, event, prom_metric=None):
    "Svc event handler"
    global update_needed
    global lock
    svc = event['object']
    ev_type = event['type']
    if not cache.is_exposed_service(svc):
        return
    if ev_type in ['ADDED', 'MODIFIED']:
        valid, cause = cache.is_valid_service(svc)
        if valid:
            if prom_metric:
                prom_metric.labels(svc.metadata.namespace, svc.metadata.name).state('valid')
            svc = await _update_service(v1_api, svc, True)
            if svc.spec.type == 'NodePort':
                # Copy here content from annotation to get ip in any case from the same field
                svc.spec.load_balancer_ip = svc.metadata.annotations['external-lb/ip-address']
            if cache.upsert_service(svc):
                async with lock:
                    update_needed = True
            return
        else:
            if prom_metric:
                prom_metric.labels(svc.metadata.namespace, svc.metadata.name).state('invalid')
            await _update_service(v1_api, svc, False, cause)
    if cache.exists_service(svc):
        if cache.delete_service(svc):
            async with lock:
                update_needed = True
    if ev_type in ['DELETED'] and prom_metric:
        prom_metric.remove(svc.metadata.namespace, svc.metadata.name)

async def watch_services(v1_api, cache, prom_metric):
    "Infinite loop that watches K8s events about services"
    while True:
        try:
            logging.debug('Full svc scan in watch mode')
            async with kubernetes.watch.Watch().stream(v1_api.list_service_for_all_namespaces,
                                            timeout_seconds=120) as stream:
                async for event in stream:
                    await handle_service_event(v1_api, cache, event, prom_metric)
        except aiohttp.ClientPayloadError as exception:
            logging.error('uNKNOWN Error: %s', exception)
        except kubernetes.client.rest.ApiException as exception:
            logging.error('ApiException: %s', exception)

async def handle_node_event(v1_api, cache, event):
    global update_needed
    global lock
    "Node event handler"
    node = event['object']
    ev_type = event['type']
    if ev_type in ['ADDED', 'MODIFIED']:
        cache.upsert_node(node)
    else:
        cache.delete_node(node)
    async with lock:
        update_needed = True

async def watch_nodes(v1_api, cache):
    "Infinite loop that watches K8s events about nodes"
    while True:
        try:
            logging.debug('Full nodes scan in watch mode')
            async with kubernetes.watch.Watch().stream(v1_api.list_node, timeout_seconds=300) as stream:
                async for event in stream:
                    await handle_node_event(v1_api, cache, event)
        except kubernetes.client.rest.ApiException as exception:
            logging.error('ApiException: %s', exception)

async def regenerate_config(daemon_controller, delay=2):
    "Infinite loop that triggers configuration regeneration"
    global update_needed
    global lock
    while daemon_controller.keep_going:
        if update_needed:
            async with lock:
                update_needed = False
            daemon_controller.sync_config()
        await asyncio.sleep(delay)
