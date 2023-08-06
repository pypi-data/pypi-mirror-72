import logging
import threading

from symmetry.clusterd.info import RedisClusterInfo
from symmetry.clusterd.monitor import NodeMonitor
from symmetry.clusterd.noded import NodeManagerDaemon
from symmetry.clusterd.policyd import BalancingPolicyDaemon
from symmetry.common.cluster import RedisNodeManager
from symmetry.routing import RedisRoutingTable

logger = logging.getLogger(__name__)


class RedisClusterDaemon:
    def __init__(self, rds) -> None:
        super().__init__()
        self.rds = rds

        self.node_manager = RedisNodeManager(rds)

        self.policyd = None
        self.noded = None
        self.monitor = None

    def run(self):
        logger.info('starting cluster daemon')

        rds = self.rds

        self.node_manager.synchronize_node_states()

        self.policyd = BalancingPolicyDaemon(RedisClusterInfo(rds), RedisRoutingTable(rds))
        self.noded = NodeManagerDaemon(self.node_manager)  # doesn't have to be started
        self.monitor = NodeMonitor(self.node_manager)

        threads = list()

        logger.info('starting policy daemon')
        policyd_thread = threading.Thread(target=self.policyd.run, name='balancing-policy-runner')
        policyd_thread.start()
        threads.append(policyd_thread)

        logger.info('starting node monitor')
        monitor_thread = threading.Thread(target=self.monitor.run, name='node-monitor-runner')
        monitor_thread.start()
        threads.append(monitor_thread)

        for t in threads:
            t.join()

        logger.debug('cluster daemon returning')

    def close(self):
        if self.monitor:
            logger.debug('closing node monitor')
            self.monitor.close()
        if self.policyd:
            logger.debug('closing policy daemon')
            self.policyd.close()
        if self.noded:
            logger.debug('closing node daemon')
            self.noded.close()
