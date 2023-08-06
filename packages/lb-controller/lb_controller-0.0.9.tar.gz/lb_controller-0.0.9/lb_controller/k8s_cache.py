"Cache for K8s objects"
import logging
import ipaddress

IP_ANNOTATION = 'external-lb/ip-address'

class K8sCache:
    "The cache"
    def __init__(self, *args):
        self.flush()
        self._ranges = []
        for arg in args:
            net = ipaddress.ip_network(arg)
            for existing_nets in self._ranges:
                assert not existing_nets.overlaps(net)
            self._ranges.append(net)

    def flush(self):
        "Empty cache"
        self._svcs = {}
        self._nodes = {}
        self._known_ips = {}

    @property
    def svcs(self):
        "Get known k8s services in cache"
        return self._svcs

    @property
    def nodes(self):
        "Get known k8s nodes in cache"
        return self._nodes

    def exists_service(self, svc):
        "Lookup for a given service in cache"
        key = f'{svc.metadata.namespace}/{svc.metadata.name}'
        return key in self._svcs

    @staticmethod
    def is_exposed_service(svc):
        "Return true if svc is exposed (is a loadbalancer or a nodeport)"
        key = f'{svc.metadata.namespace}/{svc.metadata.name}'
        if svc.spec.type not in ['LoadBalancer', 'NodePort']:
            logging.debug('Ignoring service %s because not type LoadBalancer nor NodePort %s',
                          key, svc.spec.type)
            return False
        if svc.spec.type == 'NodePort' and (svc.metadata.annotations is None or 
                IP_ANNOTATION not in svc.metadata.annotations):
            logging.debug('Ignoring NodePort service %s because not annotated', key)
            return False

        return True

    def is_valid_service(self, svc):
        """Ensure candidate svc is valid (iprange, no conflict...)
        Returns a tuple (bool, cause) cause is None if valid"""
        key = f'{svc.metadata.namespace}/{svc.metadata.name}'
        if svc.spec.type == 'NodePort':
            ip_addr = svc.metadata.annotations[IP_ANNOTATION]
        elif svc.spec.type == 'LoadBalancer':
            if svc.spec.load_balancer_ip is None:
                cause = 'no IP set in spec.loadBalancerIP field for LoadBalancer Service'
                logging.error('Invalid svc %s because %s', key, cause)
                return False, cause
            ip_addr = svc.spec.load_balancer_ip
        if ip_addr in self._known_ips and self._known_ips[ip_addr] != key:
            cause = f'IP conflicts: {ip_addr} already owned by {self._known_ips[ip_addr]}'
            logging.error('Invalid svc %s because %s', key, cause)
            return False, cause
        try:
            ip_addr = ipaddress.ip_interface(ip_addr)
            for net in self._ranges:
                if ipaddress.ip_interface(ip_addr) in net:
                    return True, None
            cause = f'IP {ip_addr} is not in a valid range'
        except ValueError:
            cause = f'IP {ip_addr} is not a valid Address'
        logging.error('Invalid svc %s because %s', key, cause)
        return False, cause

    def upsert_node(self, node):
        "Add node to cache"
        key = node.metadata.name
        logging.debug('Upsert node %s', key)
        if key in self._nodes \
                and node.metadata.resource_version == self._nodes[key].metadata.resource_version:
            logging.info('Node %s unchanged, skipping', key)
            return False
        logging.info('Node %s changed or created in cache', key)
        self._nodes[key] = node
        return True

    def delete_node(self, node):
        "delete node from cache"
        key = node.metadata.name
        logging.debug('Delete node %s', key)
        if key in self._nodes:
            del self._nodes[key]
            return True
        return False

    def upsert_service(self, svc):
        "Add service to cache"
        key = f'{svc.metadata.namespace}/{svc.metadata.name}'
        logging.debug('Upsert service %s', key)
        if key in self._svcs \
                and svc.metadata.resource_version == self._svcs[key].metadata.resource_version:
            logging.info('Service %s unchanged, skipping', key)
            return False
        logging.info('Service %s changed or created in cache', key)
        self._svcs[key] = svc
        self._known_ips[svc.spec.load_balancer_ip] = key
        return True

    def delete_service(self, svc):
        "Remove service from cache"
        key = f'{svc.metadata.namespace}/{svc.metadata.name}'
        logging.debug('Delete service %s', key)
        if key in self._svcs:
            logging.debug('Service %s deleted from cache', key)
            del self._svcs[key]
            ip_addr = svc.spec.load_balancer_ip
            if ip_addr in self._known_ips:
                del self._known_ips[ip_addr]
            return True
        return False
