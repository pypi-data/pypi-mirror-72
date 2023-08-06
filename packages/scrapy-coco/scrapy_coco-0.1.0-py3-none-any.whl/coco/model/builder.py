import logging
from typing import Dict, Any, List, Iterable, Union, Type, Callable

from coco.constants import Request as RequestConsts
from coco.exceptions import ManifestValidationError
from coco.loader import load_pipeline
from coco.model.constants import Model as ModelConsts
from coco.model.constants import ModelType
from coco.model.interface import APIModel, HTMLModel
from coco.pagination.interface import BasePagination
from coco.pagination.builder import PaginationBuilder
from coco.stage.interface import StageGroup
from coco.stage.builder import StageGroupBuilder
from coco.utils.request import DynamicRequest

LOG = logging.getLogger('coco')


class ModelBuilder:
    __slots__ = ('spec', )

    def __init__(self, spec: str) -> None:
        self.spec: Dict = spec

        for param in (ModelConsts.NAME, ModelConsts.STAGES):
            if param not in self.spec or not self.spec[param]:
                raise ManifestValidationError(
                    f'Model required attribute "{param}" is not defined or '
                    'has no value in manifest definition'
                )

        if not self.request:
            raise ManifestValidationError(
                f'Model must define "{ModelConsts.REQUEST}" specification'
            )

        if self.schedule:
            try:
                int(self.schedule)
            except ValueError:
                raise ManifestValidationError(
                    f'Model {self.name} has schedule definition '
                    f'{self.schedule}, which is not a number'
                )

        LOG.info('Model "%s" validation successful', self.name)

    def build(self) -> Iterable[Union[APIModel, HTMLModel]]:
        models: List = list()
        links: Dict[str, str] = self.request.get('links')

        for name, link in links.items():
            derived_name: str = f'{self.name}-{name}'

            request = DynamicRequest(
                method=self.request.get(
                    'method', RequestConsts.Default.METHOD
                ),
                timeout=self.request.get(
                    'timeout', RequestConsts.Default.TIMEOUT
                ),
                headers=self.request.get('headers', {}),
                cookies=self.request.get('cookies', {}),
                data=self.request.get('data', {})
            )
            models.append(
                self.cls(
                    pagination=self.pagination_instance,
                    # stages=self.stage_instances,
                    stages=self.stage_group_instances,
                    pipelines=self.pipelines,
                    schedule=self.schedule,
                    name=derived_name,
                    request=request,
                    start_link=link
                )
            )

            LOG.info('Model "%s" build successful', derived_name)

        return models

    @property
    def kind(self) -> str:
        return self.spec.get(ModelConsts.KIND, ModelType.HTML)

    @property
    def name(self) -> str:
        return self.spec.get(ModelConsts.NAME)

    @property
    def stages(self) -> List[Dict]:
        return self.spec.get(ModelConsts.STAGES)

    @property
    def stage_instances(self) -> List[StageGroup]:
        return [StageGroupBuilder(stage).build() for stage in self.stages]

    @property
    def stage_group_instances(self) -> List[List[StageGroup]]:
        stage_groups: List[List[StageGroup]] = [[]]
        request_depth: int = 0

        for stage_group_spec in self.stages:
            stage_group: StageGroup = StageGroupBuilder(stage_group_spec).build()

            if stage_group.request:
                stage_groups.append(list())
                request_depth += 1

            stage_groups[request_depth].append(stage_group)

        return stage_groups

    @property
    def delay(self) -> Union[int, float]:
        return self.spec.get(ModelConsts.DELAY, ModelConsts.Default.DELAY)

    @property
    def request(self) -> Dict[str, Any]:
        return self.spec.get(ModelConsts.REQUEST)

    @property
    def pipelines(self) -> Union[List[Callable], None]:
        raw_pipelines: str = self.spec.get(ModelConsts.PIPELINE)
        if ModelConsts.PIPELINE_DEL in raw_pipelines:
            return [
                load_pipeline(pipeline) for pipeline in map(
                    str.strip, raw_pipelines.split(ModelConsts.PIPELINE_DEL)
                )
            ]
        else:
            return [load_pipeline(raw_pipelines.strip())]

    @property
    def pagination(self) -> Dict:
        return self.spec.get(ModelConsts.PAGINATION, dict())

    @property
    def pagination_instance(self) -> BasePagination:
        return PaginationBuilder(self.pagination).build()

    @property
    def schedule(self) -> Union[int, float, None]:
        return self.spec.get(ModelConsts.SCHEDULE)

    @property
    def cls(self) -> Type[Union[APIModel, HTMLModel]]:
        return HTMLModel if self.kind == ModelType.HTML else APIModel
