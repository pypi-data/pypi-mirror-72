from typing import NamedTuple

from symmetry.api.nodes import NodeInfo


class Telemetry(NamedTuple):
    metric: str
    node: NodeInfo
    time: float
    value: object
    subsystem: str = None
