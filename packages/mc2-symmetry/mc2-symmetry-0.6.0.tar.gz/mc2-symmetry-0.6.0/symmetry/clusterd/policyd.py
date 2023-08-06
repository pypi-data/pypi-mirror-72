import inspect
import logging
import queue
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Optional

import pymq
from pymq.exceptions import RemoteInvocationError
from pymq.typing import deep_to_dict

from symmetry.api import RoutingTable, ClusterInfo, BalancingPolicy, UpdatePolicyCommand, DisablePolicyCommand, \
    BalancingPolicyService
from symmetry.clusterd import policies
from symmetry.clusterd.policies.balancing import BalancingPolicyProvider
from symmetry.common.typing import deep_from_dict, isderived

logger = logging.getLogger(__name__)


class BalancingPolicyDaemon:
    _POISON = '__POISON__'

    _rtbl: RoutingTable
    _cluster: ClusterInfo

    _queue: queue.Queue
    _runner: ThreadPoolExecutor = None
    _stopped: bool

    _policy: Optional[BalancingPolicy]
    _provider: Optional[BalancingPolicyProvider]

    def __init__(self, cluster: ClusterInfo, rtbl: RoutingTable) -> None:
        super().__init__()
        self._cluster = cluster
        self._rtbl = rtbl

        self._queue = queue.Queue()
        self._stopped = False
        self._provider = None
        self._policy = None

        self._provider_factory = policies.balancing_policy_provider_factory()

        pymq.subscribe(self._on_update_policy_command)
        pymq.subscribe(self._on_disable_policy_command)
        pymq.expose(self.get_active_policy)

    def _on_update_policy_command(self, event: UpdatePolicyCommand):
        # TODO: error handling
        policy_type = policies.balancing_policies()[event.policy]
        policy = deep_from_dict(event.parameters, policy_type)
        self.set_policy(policy)

    def _on_disable_policy_command(self, _: DisablePolicyCommand):
        self._stop_current_provider()
        self._policy = None

    def run(self):
        self._runner = ThreadPoolExecutor(max_workers=1)
        try:
            while not self._stopped:
                elem = self._queue.get()

                if elem == self._POISON:
                    break

                policy, provider = elem
                self._stop_current_provider()
                self._start_provider(provider)
                self._policy = policy
        finally:
            self._stop_current_provider()

        logger.debug('balancing daemon has stopped')

    def set_policy(self, policy: BalancingPolicy):
        if self._stopped:
            return

        logger.debug('setting new balancing policy %s', policy)
        provider = self._provider_factory(policy, self._cluster, self._rtbl)
        self._queue.put((policy, provider))

    def get_active_policy(self) -> Optional[BalancingPolicy]:
        return self._policy

    def is_provider_active(self) -> bool:
        return self._provider is not None

    def close(self):
        logger.info('closing BalancingPolicyDaemon')
        self._stopped = True
        self._queue.put(self._POISON)
        if self._runner:
            self._runner.shutdown()

    def _stop_current_provider(self):
        if self._provider:
            try:
                logger.debug('stopping current balancing policy provider %s', self._provider)
                self._provider.close()
            finally:
                self._provider = None

    def _start_provider(self, provider: BalancingPolicyProvider):
        if not self._runner:
            raise ValueError('no active runner')

        if self._provider:
            raise ValueError('current provider needs to be stopped first')

        logger.debug('starting balancing policy provider %s', provider)
        self._provider = provider
        self._runner.submit(provider.run)


class DefaultBalancingPolicyService(BalancingPolicyService):
    modules = [policies.balancing]

    def __init__(self, bus=None, modules=None) -> None:
        super().__init__()
        self.bus = bus or pymq

        if modules:
            self.modules = modules

    def get_available_policies(self):
        def is_policy(member):
            return isderived(member, BalancingPolicy)

        return {name: obj for module in self.modules for name, obj in inspect.getmembers(module, predicate=is_policy)}

    def set_active_policy(self, policy: BalancingPolicy):
        self.bus.publish(UpdatePolicyCommand(policy.name, deep_to_dict(policy)))

    def disable_active_policy(self):
        self.bus.publish(DisablePolicyCommand())

    def get_active_policy(self) -> Optional[BalancingPolicy]:
        try:
            remote = self.bus.stub(BalancingPolicyDaemon.get_active_policy, timeout=2)
            return remote()
        except RemoteInvocationError:
            logger.exception('Could not get active policy from balancing policy daemon')
            return None
