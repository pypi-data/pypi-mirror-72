import logging
from concurrent import futures

from symmetry.api import ServiceManager, ServiceMetadataRepository, NodeLister, ServiceDescription, NodeInfo, \
    ServiceInfo, ServiceStatus
from symmetry.common.cluster import is_up
from symmetry.nrg.docker import DockerGateway
from symmetry.nrg.proxy import NginxProxyConfigurator
from symmetry.nrg.ports import UnsafePortAllocator

logger = logging.getLogger(__name__)


class DefaultServiceManager(ServiceManager):
    _worker_threads: int = 4

    _nginx_config: NginxProxyConfigurator
    _docker: DockerGateway
    _metadata: ServiceMetadataRepository

    def __init__(self, metadata: ServiceMetadataRepository, node_lister: NodeLister) -> None:
        super().__init__()
        self._metadata = metadata
        self._node_lister = node_lister

        self._port_allocator = UnsafePortAllocator(metadata)
        self._nginx_config = NginxProxyConfigurator()
        self._docker = DockerGateway()

    def create(self, service: ServiceDescription):
        if self._metadata.has_service(service.id):
            raise ValueError('service exists')

        self._metadata.save_service(service)

    def describe(self, service_id: str) -> ServiceDescription:
        return self._metadata.get_service(service_id)

    def remove(self, service_id: str):
        # TODO check if has deployment, if not, raise value error (to undeploy first)
        self._metadata.remove_service(service_id)

    def deploy(self, service_id: str):
        description = self._metadata.get_service(service_id)
        if description is None:
            raise ValueError('no such service %s' % service_id)

        self._deploy_service(description)

    def undeploy(self, service_id: str):
        service = self.describe(service_id)
        if not service:
            raise ValueError('no such service %s' % service_id)
        self._undeploy_service(service)

    def destroy(self, service_id: str):
        service = self.describe(service_id)
        if not service:
            raise ValueError('no such service %s' % service_id)

        self._undeploy_service(service)
        self._metadata.remove_service(service.id)

    def _probe_container_status(self, service_id: str, node: NodeInfo):
        if not is_up(node, self._docker.docker_port):
            return 'unknown'

        containers = self._docker.list_containers(node.host)
        for container in containers:
            if container.name == service_id:
                return container.status

    def info(self, service_id: str) -> ServiceInfo:
        description = self.describe(service_id)
        if not description:
            raise ValueError('no such service %s' % service_id)

        status_list = list()

        nodes = list(self._node_lister.nodes)

        logger.debug('resolving service %s for nodes %s', service_id, [node.node_id for node in nodes])

        with futures.ThreadPoolExecutor(max_workers=self._worker_threads) as executor:
            threads = [executor.submit(self._probe_container_status, service_id, node) for node in nodes]

            futures.wait(threads, timeout=2, return_when=futures.FIRST_EXCEPTION)
            containers = [thread.result() for thread in threads]

        for i in range(len(nodes)):
            node = nodes[i]
            container = containers[i]
            status = container if container else 'created'
            status_list.append(ServiceStatus(node.node_id, status))

        return ServiceInfo(description, status_list)

    def _deploy_node_service(self, node_ip: str, service: ServiceDescription, port: int):
        self._docker.start_service_container(node_ip, service, port)
        self._nginx_config.create_entry(node_ip, service.id, port)

    def _undeploy_node_service(self, node_ip, service_id: str):
        self._docker.remove_service_container(node_ip, service_id)
        self._nginx_config.remove_entry(node_ip, service_id)

    def _deploy_service(self, service: ServiceDescription):
        if service.symmetry_port is None:
            service.symmetry_port = self._port_allocator.allocate_port()

        self._metadata.save_service(service)

        nodes = self._node_lister.nodes

        with futures.ThreadPoolExecutor(max_workers=self._worker_threads) as executor:
            threads = [executor.submit(self._deploy_node_service, n.host, service, service.symmetry_port) for n in
                       nodes]
            futures.wait(threads, return_when=futures.FIRST_EXCEPTION)
            for thread in threads:
                thread.result()

        self._metadata.set_service_hosts(service.id, *nodes)

    def _undeploy_service(self, service: ServiceDescription):
        nodes = self._node_lister.nodes
        with futures.ThreadPoolExecutor(max_workers=self._worker_threads) as executor:
            threads = [executor.submit(self._undeploy_node_service, n.host, service.id) for n in nodes]
            futures.wait(threads, return_when=futures.FIRST_EXCEPTION)
            for thread in threads:
                thread.result()
        return service
