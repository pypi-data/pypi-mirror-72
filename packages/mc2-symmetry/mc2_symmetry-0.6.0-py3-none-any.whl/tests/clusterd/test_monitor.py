import queue
import threading
import unittest
from unittest import mock
from unittest.mock import MagicMock

from pymq.provider.simple import SimpleEventBus

from symmetry.api import NodeInfo, NodeDisconnectedEvent, NodeActivatedEvent
from symmetry.clusterd.monitor import NodeMonitor


class TestNodeMonitor(unittest.TestCase):

    @mock.patch('symmetry.api.NodeLister')
    def test_emits_events_correctly(self, node_lister):
        events = queue.Queue()

        def record_disconnect(e: NodeDisconnectedEvent):
            events.put(e)

        def record_activated(e: NodeActivatedEvent):
            events.put(e)

        bus = SimpleEventBus()
        bus.subscribe(record_activated)
        bus.subscribe(record_disconnect)
        bus_t = threading.Thread(target=bus.run)
        bus_t.start()

        node_lister.nodes = [NodeInfo('node1', 'host1'), NodeInfo('node2', 'host2', ssh_port=2222)]
        fake_probe_nodes = MagicMock()

        monitor = NodeMonitor(node_lister, bus=bus)
        monitor._probe_nodes = fake_probe_nodes

        # node mode changes to True
        fake_probe_nodes.return_value = {'node1': True, 'node2': True}
        monitor.run_probe()

        event = events.get(timeout=0.5)
        self.assertIsInstance(event, NodeActivatedEvent)

        event = events.get(timeout=0.5)
        self.assertIsInstance(event, NodeActivatedEvent)

        # node mode has not changed
        fake_probe_nodes.return_value = {'node1': True, 'node2': True}
        monitor.run_probe()

        try:
            events.get(timeout=0.5)
            self.fail("Received unexpected event")
        except queue.Empty:
            pass

        # node mode of node 2 changes to False
        fake_probe_nodes.return_value = {'node1': True, 'node2': False}
        monitor.run_probe()

        event = events.get(timeout=0.5)
        self.assertEqual(event.node_id, 'node2')
        self.assertIsInstance(event, NodeDisconnectedEvent)

        # node mode of node 2 changes to True
        fake_probe_nodes.return_value = {'node1': True, 'node2': True}
        monitor.run_probe()

        event = events.get(timeout=0.5)
        self.assertEqual(event.node_id, 'node2')
        self.assertIsInstance(event, NodeActivatedEvent)

        # make sure queue is empty
        self.assertEqual(0, events.qsize())

        bus.close()
        bus_t.join(2)
