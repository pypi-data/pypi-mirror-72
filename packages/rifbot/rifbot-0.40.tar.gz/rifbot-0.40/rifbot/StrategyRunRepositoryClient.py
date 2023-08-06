from rifbot import GqlClient, RootOptions
from rifbot.gql_queries import QUERIES, SUBSCRIPTIONS, MUTATIONS
from shortid import ShortId


class StrategyRunRepositoryClient:
    def __init__(self, service: GqlClient):
        print('StrategyRunRepositoryClient')
        self.service = service

    async def findOneStrategyRun(self, options):
        print('findOneStrategyRun', 'options:', options)

        return await self.service.query(QUERIES['FIND_ONE_STRATEGY_ARCHIVE'], {
            'options': options
        })

    async def close(self):
        self.service.close()
        self.service.listen_coro.cancelled()