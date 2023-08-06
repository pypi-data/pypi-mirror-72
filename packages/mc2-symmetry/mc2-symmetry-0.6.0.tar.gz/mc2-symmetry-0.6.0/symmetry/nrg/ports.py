import abc
import time
from typing import Dict

from symmetry.api import ServiceMetadataRepository


class PortAllocator(abc.ABC):
    port_range: range = range(11000, 12000)

    def allocate_port(self) -> int:
        raise NotImplementedError


class LeasingPortAllocator(PortAllocator):
    """
    This allocator uses the service metadata repository and port leases to determine used ports, which fixes the issue
    of UnsafePortAllocator (at least for one thread). Every time a port is allocated, the allocator creates a lease for
    the port, which expires after 2 minutes. It still does not solve the problem that the port may not actually be
    available on the cluster node for which the port is being allocated.
    """
    timeout: int = 120  # 2 minutes

    def __init__(self, metadata: ServiceMetadataRepository) -> None:
        super().__init__()
        self._metadata = metadata
        self._leases: Dict[int, float] = dict()

    def _expire_leases(self):
        th = time.time() - self.timeout

        expired = {port for port, t in self._leases.items() if th > t}
        for port in expired:
            del self._leases[port]

    def allocate_port(self) -> int:
        self._expire_leases()

        ports = set(self.port_range)

        used = {int(service.symmetry_port) for service in self._metadata.get_services() if service.symmetry_port}
        leased = set(self._leases.keys())
        ports.difference_update(used, leased)

        if len(ports) == 0:
            raise ValueError('No available ports for service allocation')

        port = ports.pop()
        self._leases[port] = time.time()
        return port


class UnsafePortAllocator(PortAllocator):
    """
    Allocates ports based on which ones are registered in the metadata repository. It is unsafe because it may hand out
    the same port twice if the port has not been registered in the metadata repository before calling allocate_port
    again.
    """

    def __init__(self, metadata: ServiceMetadataRepository) -> None:
        super().__init__()
        self._metadata = metadata

    def allocate_port(self) -> int:
        ports = set(self.port_range)
        used = {int(service.symmetry_port) for service in self._metadata.get_services() if service.symmetry_port}
        ports.difference_update(used)

        if len(ports) == 0:
            raise ValueError('No available ports for service allocation')

        return ports.pop()
