import logging
from typing import List, Dict

from coco.exceptions import SuppressStage
from coco.constants import Const
from coco.utils.request import DynamicRequest

LOG = logging.getLogger('coco')


class Stage:
    def __init__(self, selector, name=None, pipelines=None, prop=Const.TEXT):
        self.name = name
        self.selector = selector
        self.prop = prop or Const.TEXT
        self.pipelines = pipelines or list()

    async def extract(self, context):
        result = list()

        for element in context.select(self.selector):
            result.append(await self.extract_value(element))

        if not result:
            return {self.name: Const.NA}
        elif len(result) == 1:
            return result[0]
        else:
            return {self.name: [x[self.name] for x in result]}

    async def extract_value(self, element):
        if self.prop == Const.TEXT:
            result = element.get_text()
        elif self.prop == Const.HTML:
            result = str(element)
        else:
            result = element.get(self.prop)

        for pipeline in self.pipelines:
            result = await pipeline(result)

        return {self.name: result}

    def __bool__(self):
        """denotes if stage is extractable"""
        return bool(self.selector and self.prop and self.name)

    def __str__(self):
        if self.prop and self.selector:
            return f'{self.selector}[{self.prop}] as {self.name}'
        return f'{self.name}'

    def __repr__(self):
        return str(self)


class StageGroup:
    def __init__(self, stages, request=None):
        self.stages = stages
        self.request: DynamicRequest = request

        self.results = None  # NOTE - consider remove from instance vars
        self.main_stage = stages.pop(0)

    async def extract(self, context):
        self.results: List = list()

        base_data: Dict = dict()
        if self.main_stage:  # NOTE - if stage is executable
            base_data = await self.main_stage.extract(context)

        for sub_container in context.select(self.main_stage.selector):
            try:
                temp: Dict = base_data.copy()

                for sub_stage in self.stages:
                    temp.update(await sub_stage.extract(sub_container))

                self.results.append(temp)
            except SuppressStage:
                LOG.debug('%s: suppressing item', str(self))

    def __str__(self):
        return str(self.main_stage)

    def __repr__(self):
        return str(self)
