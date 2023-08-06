import asyncio
import logging
from typing import Dict, Union

from coco.constants import Request as RequestConsts
from coco.utils.timer import TimeLog


class DynamicRequest:
    __slots__ = ('key', 'method', 'timeout', 'data', 'headers', 'cookies',
                 'session', 'delay')

    def __init__(self,
                 key: Union[None, str] = None,
                 method: str = RequestConsts.Default.METHOD,
                 timeout: int = 3000,
                 **kw: Dict) -> None:
        self.key: str = key
        self.method: str = method
        self.timeout: int = timeout

        self.data: Dict = kw.get('data', dict())
        self.headers: Dict = kw.get('headers', dict())
        self.cookies: Dict = kw.get('cookies', dict())
        self.delay: int = kw.get('delay', 0)

        self.session = getattr(asyncio.get_running_loop(), 'session')
        if not self.session:
            raise AttributeError('Event loop has no attribute "session"')

    async def fetch(self, item=None, link=None):
        if self.key and not item:
            raise ValueError('DynamicRequest.fetch must receive item: Dict')
        if not self.key and not link:
            raise ValueError('DynamicRequest.fetch must receive link: str')
        if self.delay:
            await asyncio.sleep(self.delay)

        link: str = item.get(self.key) if item else link
        request = self.session.request(
            timeout=self.timeout,
            headers=self.headers,
            method=self.method,
            json=self.data,
            url=link
        )
        async with TimeLog(f'{str(self)}: {link} fetch', logging.DEBUG):
            async with request as response:
                return await response.text()

    def __str__(self):
        return f'DynamicRequest[{self.key}]'

    def __repr__(self):
        return str(self)
