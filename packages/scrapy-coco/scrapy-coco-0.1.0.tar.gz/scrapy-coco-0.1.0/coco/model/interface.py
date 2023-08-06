import asyncio
import logging
from functools import partial
from typing import List, Union, Callable

from aiohttp.client_exceptions import InvalidURL
from bs4 import BeautifulSoup
import json

from coco.exceptions import (NextPageNotFoundError,
                             PaginationPageThresholdReached)
from coco.pagination.interface import BasePagination, DummyPagination
from coco.stage.interface import StageGroup
from coco.utils.request import DynamicRequest
from coco.utils.timer import TimeLog, timelog

LOG = logging.getLogger('coco')


class Model:
    __slots__ = ('name', 'start_link', 'stages', 'request', 'pagination',
                 'pipelines', 'schedule', 'context', 'results')

    def __init__(self,
                 name: str,
                 start_link: str,
                 stages: List[StageGroup],
                 request: DynamicRequest,
                 pagination: BasePagination = DummyPagination(),
                 pipelines: Union[List[Callable], None] = None,
                 schedule: Union[float, int, None] = None) -> None:
        # NOTE - required instance variables
        self.name: str = name
        self.start_link: str = start_link
        self.stages: List[StageGroup] = stages
        # NOTE - optional instance variables
        self.request: DynamicRequest = request
        self.pagination = pagination
        self.pipelines: Union[List[Callable], None] = pipelines
        self.schedule: Union[float, int, None] = schedule
        # internally used instance variables
        self.context = None
        self.results = list()

    async def run(self) -> None:
        if self.schedule:
            while True:
                async with TimeLog(f'{str(self)}:'):
                    await self._run()

                LOG.info('%s: re-scheduling after %ss', self, self.schedule)
                await asyncio.sleep(self.schedule)
                self.cleanup()
        else:
            await self._run()

    async def _run(self) -> None:
        next_page_link: str = self.start_link

        while next_page_link:
            try:
                self.context = self.context_loader(
                    await self.request.fetch(link=next_page_link)
                )
                await self.run_stages()
                await self.run_pipelines()
                next_page_link = self.pagination.get_next_page(next_page_link)
                LOG.info(
                    '%s: next page found (%s)',
                    str(self),
                    self.pagination.page
                )
            except NextPageNotFoundError:
                LOG.info('%s: Next page not found', str(self))
                break
            except PaginationPageThresholdReached:
                LOG.info(
                    '%s: page threshold (%s) reached',
                    str(self),
                    self.pagination.page
                )
                break
            except Exception as ex:
                LOG.exception(ex)

    @timelog('stages')
    async def run_stages(self):
        for sgc_index, stage_groups in enumerate(self.stages):
            if sgc_index == 0:
                for stage_group in stage_groups:
                    await stage_group.extract(self.context)
                    if not self.results:
                        self.results.extend(stage_group.results)
                    else:
                        for idx in range(len(stage_group.results)):
                            self.results[idx].update(stage_group.results[idx])
            else:
                for res_index, result in enumerate(self.results):
                    first_stage_group = stage_groups[0]
                    try:
                        self.context = self.context_loader(
                            await first_stage_group.request.fetch(item=result)
                        )
                    except InvalidURL as invalid_url:
                        LOG.exception(invalid_url)
                        continue

                    for stage_group in stage_groups:
                        await stage_group.extract(self.context)
                        self.results[res_index].update(stage_group.results[0])

    @timelog('pipelines')
    async def run_pipelines(self) -> None:
        if self.pipelines:
            if len(self.pipelines) > 1:
                for pipeline in self.pipelines[:-1]:
                    self.results = await pipeline(self, self.results)
            await self.pipelines[-1](self, self.results)
        self.results = list()

    def cleanup(self) -> None:
        """method for cleaning model up, before re-schedule"""
        if self.pagination:
            self.pagination.reset()

    @property
    def context_loader(self) -> Callable:
        raise NotImplementedError

    def __str__(self) -> str:
        return f'Model {self.name}'

    def __repr__(self) -> str:
        return str(self)


class HTMLModel(Model):
    __slots__ = tuple()

    @property
    def context_loader(self):
        return partial(BeautifulSoup, features='lxml')


class APIModel(Model):
    __slots__ = tuple()

    @property
    def context_loader(self):
        return json.loads
