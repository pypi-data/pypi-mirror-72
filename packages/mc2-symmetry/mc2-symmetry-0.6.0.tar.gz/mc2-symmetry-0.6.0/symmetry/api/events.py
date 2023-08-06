from typing import NamedTuple


class NodeCreatedEvent(NamedTuple):
    node_id: str


class NodeUpdatedEvent(NamedTuple):
    node_id: str


class NodeRemovedEvent(NamedTuple):
    node_id: str


class NodeDisconnectedEvent(NamedTuple):
    node_id: str


class NodeActivatedEvent(NamedTuple):
    node_id: str


class BootNodeCommand(NamedTuple):
    node_id: str


class ShutdownNodeCommand(NamedTuple):
    node_id: str


class SuspendNodeCommand(NamedTuple):
    node_id: str

