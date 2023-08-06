import abc
from typing import NamedTuple, List, Dict, Optional


class NodeInfo(NamedTuple):
    node_id: str
    host: str
    mac: str = None
    user: str = None
    ssh_port: int = 22

    def get_host_string(self):
        if self.user:
            return "%s@%s:%d" % (self.user, self.host, self.ssh_port)
        else:
            return "%s:%d" % (self.host, self.ssh_port)


class NodeLister(abc.ABC):

    @property
    def nodes(self) -> List[NodeInfo]:
        raise NotImplementedError


class NodeManager(NodeLister):

    @property
    def nodes(self) -> List[NodeInfo]:
        return self.get_nodes()

    def save_node(self, node: NodeInfo) -> bool:
        """
        Creates or updates the given node.

        :param node: the node to save
        :return: true if the node was created, false if it was updated
        """
        raise NotImplementedError

    def remove_node(self, node_id: str) -> bool:
        raise NotImplementedError

    def has_node(self, node_id: str) -> bool:
        raise NotImplementedError

    def get_nodes(self) -> List[NodeInfo]:
        raise NotImplementedError

    def get_node(self, node_id: str) -> Optional[NodeInfo]:
        for node in self.get_nodes():
            if node.node_id == node_id:
                return node

    def set_node_state(self, node_id: str, state: str):
        raise NotImplementedError

    def get_node_states(self) -> Dict[str, str]:
        raise NotImplementedError

    def synchronize_node_states(self):
        raise NotImplementedError
