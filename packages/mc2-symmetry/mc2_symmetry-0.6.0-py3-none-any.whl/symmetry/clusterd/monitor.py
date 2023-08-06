import logging
from typing import Dict

import pymq

from symmetry.api import NodeLister, NodeActivatedEvent, NodeDisconnectedEvent
from symmetry.common.cluster import probe_nodes
from symmetry.common.scheduler import Scheduler

logger = logging.getLogger(__name__)


class NodeMonitor:
    """
    The node monitor periodically pings nodes returned by a NodeLister and emits appropriate state update events on a
    pymq EventBus.
    """

    def __init__(self, nodes: NodeLister, bus: pymq.EventBus = None):
        self.scheduler = Scheduler()
        self.nodes = nodes
        self.bus = bus if bus else pymq

        self._previous_states: Dict[str, bool] = dict()

    def run(self):
        # initialize states
        self._previous_states = self._probe_nodes()

        # schedule probe
        self.scheduler.schedule(self.run_probe, period=5, fixed_rate=False)
        self.scheduler.run()

    def close(self):
        self.scheduler.close()

    def _probe_nodes(self):
        nodes = self.nodes.nodes
        logger.debug('running probe for nodes %s', nodes)
        return probe_nodes(nodes)

    @property
    def states(self) -> Dict[str, bool]:
        return dict(self._previous_states)

    def run_probe(self):
        current = self._probe_nodes()
        previous = self._previous_states

        node_ids = set()
        node_ids.update(current.keys())
        node_ids.update(previous.keys())

        for node_id in node_ids:
            current_state = current.get(node_id)
            previous_state = previous.get(node_id)

            if current_state is None:
                # a node has become stale (was measured previously, but was removed)
                logger.warning('node was removed %s', node_id)
                continue

            if current_state == previous_state:
                # nothing has changed
                continue

            if current_state:
                # node has come online
                self._emit_node_activated(node_id)
            else:
                # node has gone offline
                self._emit_node_disconnected(node_id)

        self._previous_states = dict(current)

    def _emit_node_disconnected(self, node_id):
        logger.debug('emitting node disconnected event %s', node_id)
        self.bus.publish(NodeDisconnectedEvent(node_id))

    def _emit_node_activated(self, node_id):
        logger.debug('emitting node activated event %s', node_id)
        self.bus.publish(NodeActivatedEvent(node_id))
