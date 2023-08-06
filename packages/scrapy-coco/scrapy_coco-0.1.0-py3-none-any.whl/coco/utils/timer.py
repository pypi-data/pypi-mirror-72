import logging
from time import time

LOG = logging.getLogger('coco')


class TimeLog:
    __slots__ = ('start_time', 'level', 'start', 'message')

    def __init__(self, message, level: int = None) -> None:
        self.level = level or LOG.getEffectiveLevel()
        self.start: float = 0
        self.message: str = message

    async def __aenter__(self) -> None:
        self.start: float = time()

    async def __aexit__(self, *_, **__) -> None:
        diff: float = time() - self.start
        LOG.log(self.level, '%s executed in %.2fs', self.message, diff)


# async def timelog(message: str, level: int = logging.DEBUG):
#     async def _timelog(function):
#         async def wrapper(self, *a, **kw)
#             async with TimeLog(f'{str(self)}: {message}', level):
#                 return await function(self, *a, **kw)
#         return await wrapper
#     return await _timelog

def timelog(message: str, level: int = logging.DEBUG):
    def _timelog(coro):
        async def wrapper(self, *a, **kw):
            async with TimeLog(f'{str(self)}: {message}', level):
                return await coro(self, *a, **kw)
        return wrapper
    return _timelog
