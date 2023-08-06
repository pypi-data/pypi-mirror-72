from typing import List, Union

from coco.constants import Request as RequestConsts
from coco.exceptions import ManifestValidationError
from coco.loader import load_pipeline
from coco.stage.constants import Stage as StageConsts
from coco.stage.interface import Stage, StageGroup
from coco.utils.request import DynamicRequest


class StageBuilder:
    def __init__(self, raw):
        self.raw = raw
        self.name = None
        self.pipelines = None
        self.selector = None
        self.prop = None

        temp = self.raw

        # NOTE - extract stage name
        delimiter = f' {StageConsts.NAME_DEL} '
        if delimiter in temp:
            temp, self.name = map(str.strip, self.raw.split(delimiter))

        # NOTE - extract pipelines
        delimiter = StageConsts.PIPELINE_DEL
        if delimiter in temp:
            temp, self.pipelines = map(str.strip, temp.split(delimiter, 1))
            self.pipelines = map(str. strip, self.pipelines.split(delimiter))
            self.pipelines = [load_pipeline(p) for p in self.pipelines]

        # NOTE - extract selector & attribute
        # TODO - missing API stage type distinguisher here
        delimiter = StageConsts.ATTR_DEL
        if delimiter in temp:
            self.selector, self.prop = map(
                str.strip, temp.split(delimiter)
            )
        else:
            self.selector, self.prop = temp, None

    def build(self):
        return Stage(selector=self.selector, prop=self.prop, name=self.name,
                     pipelines=self.pipelines)


class StageGroupBuilder:
    def __init__(self, spec):
        self.spec = spec

    def build(self) -> StageGroup:
        stages = [StageBuilder(self.selector).build()]

        for sub_stage in self.sub_stages:
            stages.append(sub_stage.build())

        return StageGroup(stages=stages, request=self.request)

    @property
    def selector(self) -> str:
        if StageConsts.SELECTOR not in self.spec:
            raise ManifestValidationError('Stage must contain selector')
        return self.spec.get('selector')

    @property
    def request(self):
        request = self.spec.get(StageConsts.REQUEST)
        if request:
            return DynamicRequest(
                key=request.get(RequestConsts.KEY),
                method=request.get(
                    RequestConsts.METHOD,
                    RequestConsts.Default.METHOD
                ),
                timeout=request.get(
                    RequestConsts.TIMEOUT,
                    RequestConsts.Default.TIMEOUT
                ),
                headers=request.get(RequestConsts.HEADERS),
                cookies=request.get(RequestConsts.COOKIES),
                data=request.get(RequestConsts.DATA)
            )
        return None

    @property
    def sub_stages(self):
        sub_stages = self.spec.get(StageConsts.SUB_STAGES)
        if self.has_sub_stages and not sub_stages:
            raise ManifestValidationError(
                'StageGroup stages must not be empty'
            )
        return [StageBuilder(s) for s in sub_stages]

    @property
    def has_sub_stages(self):
        return bool(self.spec.get(StageConsts.SUB_STAGES))