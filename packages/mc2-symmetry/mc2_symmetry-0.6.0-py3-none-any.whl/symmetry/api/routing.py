import abc
from typing import NamedTuple, List, Dict, Optional, Any


class RoutingRecord(NamedTuple):
    service: str
    hosts: List[str]
    weights: List[float]


class RoutingTable(abc.ABC):
    def get_routing(self, service) -> RoutingRecord:
        raise NotImplementedError

    def set_routing(self, record: RoutingRecord):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def list_services(self):
        raise NotImplementedError

    def remove_service(self, service):
        raise NotImplementedError

    def get_routes(self):
        return [self.get_routing(service) for service in self.list_services()]


class Balancer(abc.ABC):

    def next_host(self, service=None):
        raise NotImplementedError


class BalancingPolicy:
    name: str


class UpdatePolicyCommand:
    policy: str
    parameters: Dict[str, Any]

    def __init__(self, policy: str, parameters: Dict[str, Any]) -> None:
        super().__init__()
        self.policy = policy
        self.parameters = parameters


class DisablePolicyCommand:
    pass


class BalancingPolicyService:

    def get_available_policies(self) -> Dict:
        raise NotImplementedError

    def set_active_policy(self, policy: BalancingPolicy):
        raise NotImplementedError

    def disable_active_policy(self):
        raise NotImplementedError

    def get_active_policy(self) -> Optional[BalancingPolicy]:
        raise NotImplementedError

    def get_policy(self, name: str) -> Optional[BalancingPolicy]:
        return self.get_available_policies().get(name, None)
