import inspect
from typing import Dict

from symmetry.api import BalancingPolicy
from symmetry.clusterd.policies.balancing import RoundRobin, NodeWeight, Weighted, ReactiveAutoscaling, \
    BalancingPolicyProvider, RoundRobinProvider, WeightedProvider, ReactiveAutoscalingProvider, BalancingPolicyProvider
from symmetry.common.typing import isderived

__all__ = [
    'BalancingPolicyProvider',
    'RoundRobin',
    'NodeWeight',
    'Weighted',
    'ReactiveAutoscaling',
    'BalancingPolicyProvider',
    'RoundRobinProvider',
    'WeightedProvider',
    'ReactiveAutoscalingProvider',
    'balancing_policies',
    'balancing_policy_providers',
    'balancing_policy_provider_factory'
]


def balancing_policies() -> Dict[str, BalancingPolicy]:
    def is_policy(member):
        return isderived(member, BalancingPolicy)

    return {name: obj for name, obj in inspect.getmembers(balancing, predicate=is_policy)}


def balancing_policy_providers() -> Dict[str, type]:
    def is_provider(obj):
        return isderived(obj, balancing.BalancingPolicyProvider)

    providers = dict()

    for name, cls in inspect.getmembers(balancing, predicate=is_provider):
        provider_type = cls
        policy_type = cls.__annotations__['policy']

        providers[policy_type.name] = provider_type

    return providers


def balancing_policy_provider_factory():
    providers = balancing_policy_providers()

    def factory(policy, *args, **kwargs):
        if policy.name not in providers:
            raise ValueError(f'Unknown policy {policy.name}')

        return providers[policy.name](policy, *args, **kwargs)

    return factory
