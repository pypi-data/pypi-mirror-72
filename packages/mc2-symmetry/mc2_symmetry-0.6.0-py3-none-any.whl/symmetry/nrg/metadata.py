from typing import List, Set

import redis
from redis.client import Pipeline

from symmetry.api import ServiceMetadataRepository, ServiceDescription, NodeInfo


class RedisServiceMetadataRepository(ServiceMetadataRepository):
    rds: redis.Redis

    '''
    symmetry:services = set
    symmetry:service:{service} = hash (ServiceDescription)
    symmetry:service:{service}:hosts = set
    '''

    def __init__(self, rds: redis.Redis) -> None:
        super().__init__()
        self.rds = rds

    def save_service(self, service: ServiceDescription) -> bool:
        pipe = self.rds.pipeline()
        self._pipeline_save_service(service, pipe)
        result = pipe.execute()

        return result[0] == 1

    def remove_service(self, service_id: str) -> bool:
        pipe = self.rds.pipeline()
        pipe.srem('symmetry:services', service_id)
        pipe.delete(f'symmetry:service:{service_id}', f'symmetry:service:{service_id}:hosts')
        result = pipe.execute()

        return result[0] == 1

    def has_service(self, service_id: str) -> bool:
        return self.rds.sismember('symmetry:services', service_id)

    def get_services(self) -> List[ServiceDescription]:
        pipe = self.rds.pipeline()

        for service_id in list(self.rds.smembers('symmetry:services')):
            hkey = f'symmetry:service:{service_id}'
            pipe.hgetall(hkey)

        result = pipe.execute()
        return [ServiceDescription(**item) for item in result if item]

    def set_service_hosts(self, service_id: str, *args: NodeInfo):
        pipe = self.rds.pipeline()

        for node in args:
            pipe.sadd(f'symmetry:services:{service_id}:hosts', node.host)

        pipe.execute()

    def get_service_hosts(self, service_id: str) -> Set[str]:
        pipe = self.rds.pipeline()

        pipe.smembers(f'symmetry:service:{service_id}:hosts')

        result = pipe.execute()
        return result[0]

    @staticmethod
    def _pipeline_save_service(service: ServiceDescription, pipe: Pipeline):
        pipe.sadd('symmetry:services', service.id)
        hkey = f'symmetry:service:{service.id}'
        for k, v in service.__dict__.items():
            if v is None:
                pipe.hdel(hkey, k)
                continue
            pipe.hset(hkey, k, v)
