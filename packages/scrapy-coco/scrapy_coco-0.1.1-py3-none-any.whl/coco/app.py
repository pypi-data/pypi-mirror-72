import asyncio
import json
import logging
import os
from functools import cached_property
from typing import List, Iterator

from aiohttp import ClientSession, TCPConnector

from coco.exceptions import ManifestLoadError
from coco.model.builder import ModelBuilder

try:
    LOG_LEVEL: int = int(os.environ.get('COCO_LOG_LEVEL', logging.DEBUG))
except ValueError:
    LOG_LEVEL: int = logging.DEBUG

logging.basicConfig(
    level=LOG_LEVEL,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %I:%M:%S',
    handlers=[
        logging.FileHandler('coco.log', 'w', 'utf8'),
        logging.StreamHandler()
    ]
)
LOG = logging.getLogger('coco')


class ManifestLoader:
    def __init__(self, manifest_dir: str) -> None:
        self.manifest_dir = manifest_dir
        self._manifests: List = list()

    def __discover(self) -> None:
        for mfile in filter(lambda x: x.endswith('.json'),
                            os.listdir(self.manifest_dir)):
            self._manifests.append(mfile)
        LOG.info('Discovered: %s', json.dumps(self._manifests, indent=4))

    @property
    def manifests(self) -> List:
        if not self._manifests:
            self.__discover()
        return self._manifests

    @property
    def manifest_dir(self) -> str:
        return self._manifest_dir

    @manifest_dir.setter
    def manifest_dir(self, value: str):
        if not value or not os.path.isdir(value):
            raise ManifestLoadError(f'{self.manifest_dir} is not a directory')
        self._manifest_dir = value

    @cached_property
    def model_builders(self) -> Iterator:
        for file in self.manifests:
            with open(os.path.join(self.manifest_dir, file), 'r') as stream:
                yield ModelBuilder(json.load(stream))

    @cached_property
    def models(self) -> Iterator:
        for model_builder in self.model_builders:
            yield from model_builder.build()


class Application:
    __slots__ = ('limit_per_host', 'total_limit', 'manifest_loader', '_loop')

    def __init__(self, manifest_dir: str) -> None:
        self.total_limit: int = 10
        self.limit_per_host: int = 2
        self.manifest_loader: ManifestLoader = ManifestLoader(manifest_dir)
        # initialize event loop and attach ClientSession
        self._loop = asyncio.get_event_loop()
        connector = TCPConnector(
            limit_per_host=self.limit_per_host,
            limit=self.total_limit
        )
        self._loop.session = ClientSession(
            connector=connector,
            loop=self._loop
        )

    def __call__(self):
        LOG.info('coco - keep things scraped')
        self._loop.run_until_complete(self.run_service())
        LOG.info('coco out! bye')

    async def run_service(self):
        await asyncio.gather(*[
            model.run() for model in self.manifest_loader.models
        ])
