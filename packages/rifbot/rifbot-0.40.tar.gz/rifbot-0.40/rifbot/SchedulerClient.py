import asyncio
from rifbot import GqlClient, RootOptions
from rifbot.gql_queries import QUERIES, SUBSCRIPTIONS, MUTATIONS
from shortid import ShortId
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)


class SchedulerClient:
    def __init__(self, service: GqlClient):
        print('SchedulerClient')
        self.service = service

    async def enqueueStrategyRun(self, rootOptions: RootOptions, runId: str = None):
        if runId is None:
            runId = ShortId().generate()

        return await self.service.mutate(MUTATIONS['ENQUEUE_STRATEGY_RUN'], {
            'rootOptions': rootOptions.__dict__,
            'runId': runId,
        })

    async def close(self):
        self.service.close()
        self.service.listen_coro.cancelled()
