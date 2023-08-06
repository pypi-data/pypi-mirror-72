from typing import List, Optional

from telemc import TelemetrySubscriber

from symmetry.api import ClusterInfo, RoutingTable, ServiceMetadataRepository, NodeInfo
from symmetry.common.cluster import RedisNodeManager
from symmetry.nrg import RedisServiceMetadataRepository
from symmetry.routing import RedisRoutingTable


class RedisClusterInfo(ClusterInfo):
    node_manager: RedisNodeManager
    rtbl: RoutingTable
    service_repository: ServiceMetadataRepository
    telemc: TelemetrySubscriber

    def __init__(self, rds) -> None:
        super().__init__()
        self.rds = rds
        self.node_manager = RedisNodeManager(rds)
        self.rtbl = RedisRoutingTable(rds)
        self.telemc = TelemetrySubscriber(rds)
        self.service_repository = RedisServiceMetadataRepository(rds)

    @property
    def nodes(self) -> List[str]:
        return self.node_manager.get_node_ids()

    def node_info(self, node_id) -> Optional[NodeInfo]:
        return self.node_manager.get_node(node_id)

    @property
    def active_nodes(self) -> List[str]:
        states = self.node_manager.get_node_states()
        return [node for node, state in states.items() if state == 'online']

    @property
    def services(self) -> List[str]:
        services = self.service_repository.get_services()
        return [service.id for service in services]
