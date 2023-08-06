import abc
from io import BytesIO
from typing import NamedTuple, List, Set

from symmetry.api.nodes import NodeInfo


class ServiceDescription:
    id: str
    name: str
    image: str
    port: str
    command: str = None
    version: str = None
    description: str = None
    maintainer: str = None
    image_file: BytesIO = None
    symmetry_port: str = None  # FIXME

    def __init__(self, id: str, name: str, image: str, port: str, command: str = None, version: str = None,
                 description: str = None, maintainer: str = None, image_file: BytesIO = None,
                 symmetry_port: str = None) -> None:
        super().__init__()
        self.id = id
        self.name = name
        self.image = image
        self.port = port
        self.command = command
        self.version = version
        self.description = description
        self.maintainer = maintainer
        self.image_file = image_file
        self.symmetry_port = symmetry_port


class ServiceStatus(NamedTuple):
    node: str

    '''
    CREATED
    DEPLOYED
    RUNNING
    UNKNOWN
    '''
    status: str


class ServiceInfo(NamedTuple):
    description: ServiceDescription
    status: List[ServiceStatus]


class ServiceMetadataRepository(abc.ABC):

    def save_service(self, service: ServiceDescription) -> bool:
        """
        Creates or updates the given service.

        :param service: the node to save
        :return: true if the service was created, false if it was updated
        """
        raise NotImplementedError

    def remove_service(self, service_id: str) -> bool:
        raise NotImplementedError

    def has_service(self, service_id: str) -> bool:
        raise NotImplementedError

    def get_services(self) -> List[ServiceDescription]:
        raise NotImplementedError

    def get_service(self, service_id: str) -> ServiceDescription:
        for service in self.get_services():
            if service.id == service_id:
                return service

    def set_service_hosts(self, service_id: str, *args: NodeInfo):
        raise NotImplementedError

    def get_service_hosts(self, service_id: str) -> Set[str]:
        raise NotImplementedError


class ServiceManager(abc.ABC):

    def create(self, service: ServiceDescription):
        raise NotImplementedError

    def describe(self, service_id: str) -> ServiceDescription:
        raise NotImplementedError

    def remove(self, service_id: str):
        raise NotImplementedError

    def deploy(self, service_id: str):
        raise NotImplementedError

    def undeploy(self, service_id: str):
        raise NotImplementedError

    def destroy(self, service_id: str):
        raise NotImplementedError

    def info(self, service_id: str) -> ServiceInfo:
        raise NotImplementedError
