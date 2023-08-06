import abc
from typing import List, Iterable, Optional

from symmetry.api.nodes import NodeInfo


class ClusterInfo(abc.ABC):

    @property
    def nodes(self) -> List[str]:
        raise NotImplementedError

    def node_info(self, node_id: str) -> Optional[NodeInfo]:
        raise NotImplementedError

    @property
    def active_nodes(self) -> List[str]:
        raise NotImplementedError

    @property
    def services(self) -> List[str]:
        raise NotImplementedError


class ClusterGateway(abc.ABC):

    @property
    def nodes(self) -> Iterable[NodeInfo]:
        raise NotImplementedError

    def boot(self, nodes: List[str] = None):
        raise NotImplementedError

    def shutdown(self, nodes: List[str] = None):
        raise NotImplementedError

    def suspend(self, nodes: List[str] = None):
        raise NotImplementedError

    def probe_node_states(self, nodes: List[str] = None):
        raise NotImplementedError

    def select_nodes(self, nodes: Iterable[str]):
        if not nodes:
            return self.nodes

        return [node for node in self.nodes if node.node_id in nodes]
