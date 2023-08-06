import logging
import socket
import threading
from collections import defaultdict
from concurrent.futures.thread import ThreadPoolExecutor

import pymq
import wakeonlan

from symmetry.api import NodeManager, BootNodeCommand, ShutdownNodeCommand, SuspendNodeCommand, NodeInfo
from symmetry.common.cluster import NodeStateUpdateListener, is_up, create_connection
from symmetry.common.ssh import ExecutionException

logger = logging.getLogger(__name__)


class NodeManagerDaemon:
    node_manager: NodeManager

    def __init__(self, node_manager: NodeManager) -> None:
        super().__init__()
        self.node_manager = node_manager
        self.node_state_updater = NodeStateUpdateListener(node_manager)

        self.executor = ThreadPoolExecutor()
        self.locks = defaultdict(threading.Lock)
        pymq.subscribe(self._on_boot_node_command)
        pymq.subscribe(self._on_shutdown_node_command)
        pymq.subscribe(self._on_suspend_node_command)

    def close(self):
        logger.debug('closing NodeManagerDaemon')

        self.node_state_updater.close()

        pymq.unsubscribe(self._on_boot_node_command)
        pymq.unsubscribe(self._on_shutdown_node_command)
        pymq.unsubscribe(self._on_suspend_node_command)

        self.executor.shutdown()

    def _on_boot_node_command(self, cmd: BootNodeCommand):
        logger.debug('received boot command for node %s', cmd.node_id)

        node = self.node_manager.get_node(cmd.node_id)
        if not node:
            return
        self.executor.submit(self._do_boot, node)

    def _on_shutdown_node_command(self, cmd: ShutdownNodeCommand):
        logger.debug('received shutdown command for node %s', cmd.node_id)

        node = self.node_manager.get_node(cmd.node_id)
        if not node:
            return
        self.executor.submit(self._do_shutdown, node)

    def _on_suspend_node_command(self, cmd: SuspendNodeCommand):
        logger.debug('received suspend command for node %s', cmd.node_id)

        node = self.node_manager.get_node(cmd.node_id)
        if not node:
            return
        self.executor.submit(self._do_suspend, node)

    def _do_boot(self, node: NodeInfo):
        logger.info('sending magic packet to %s: %s', node.node_id, node.mac)
        wakeonlan.send_magic_packet(node.mac)

    def _do_shutdown(self, node: NodeInfo):
        with self.locks[node.node_id]:
            if not is_up(node):
                logger.debug('received shutdown command, but node was offline %s', node.node_id)
                return

            con = create_connection(node)
            con.kwargs['timeout'] = 5
            con.kwargs['banner_timeout'] = 5
            con.kwargs['auth_timeout'] = 5

            logger.info('attempting to shut down node %s', node.node_id)
            con.ensure_connection()
            try:
                con.run('shutdown -h now', timeout=5)
            except:
                if logger.isEnabledFor(logging.DEBUG):
                    logger.exception('could not shut down node %s', node)
            finally:
                con.close()

    def _do_suspend(self, node: NodeInfo):
        with self.locks[node.node_id]:
            if not is_up(node):
                logger.debug('received suspend command, but node was offline %s', node.node_id)
                return

            con = create_connection(node)
            con.kwargs['timeout'] = 5
            con.kwargs['banner_timeout'] = 5
            con.kwargs['auth_timeout'] = 5

            logger.info('attempting to suspend node %s', node.node_id)
            con.ensure_connection()
            try:
                # https://askubuntu.com/questions/1792/how-can-i-suspend-hibernate-from-command-line
                con.run('systemctl suspend', timeout=5)
                logger.debug('suspend command returned')
            except ExecutionException as e:
                if isinstance(e.result.error, socket.timeout):
                    logger.debug('command timed out as expected')
                else:
                    if logger.isEnabledFor(logging.DEBUG):
                        logger.exception('could not shut down node %s', node)
            finally:
                logger.debug('closing connection')
                con.close()
