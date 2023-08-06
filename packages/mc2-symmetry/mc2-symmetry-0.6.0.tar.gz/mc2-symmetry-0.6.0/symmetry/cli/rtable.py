import pymq
from pymq.provider.redis import RedisConfig

from symmetry.common import config
from symmetry.routing import RedisRoutingTable
from symmetry.routing.shell import RouterShell


def main():
    rds = config.get_redis()
    pymq.init(RedisConfig(rds))

    shell = RouterShell(RedisRoutingTable(rds))
    shell.run()


if __name__ == '__main__':
    main()
