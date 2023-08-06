import logging
from typing import Dict
from urllib.parse import ParseResult
from urllib.parse import urlparse as parse_url

from coco.exceptions import (NextPageNotFoundError,
                             PaginationPageThresholdReached)

LOG = logging.getLogger('coco')


class BasePagination:
    __slots__ = ('_page', 'page_threshold', 'init_page_num')

    def __init__(self, page_threshold: int = 1, init_page_num: int = 1):
        self.page_threshold: int = page_threshold
        self.init_page_num: int = init_page_num
        self.page: int = init_page_num

    def get_next_page(self, current_link: str, **kw: Dict) -> str:
        raise NotImplementedError('get_next_page method must be implemented')

    def reset(self) -> None:
        self.page = self.init_page_num

    @property
    def page(self) -> int:
        return self._page

    @page.setter
    def page(self, value: int):
        if value > self.page_threshold:
            raise PaginationPageThresholdReached
        self._page = value

    def __str__(self):
        return f'Pagination @page N{self.page}'


class DummyPagination(BasePagination):
    __slots__ = tuple()

    def get_next_page(self, current_link: str, **kw: Dict) -> str:
        raise NextPageNotFoundError


class OnsitePagination(BasePagination):
    __slots__ = ('selector', 'prop')

    def __init__(self,
                 selector: str,
                 prop: str,
                 page_threshold: int = 1,
                 init_page_num: int = 1) -> None:
        super().__init__(page_threshold, init_page_num)
        self.selector: str = selector
        self.prop: str = prop

    def get_next_page(self, current_link: str, **kw) -> str:
        self.page += 1
        cur_page_flag: bool = False
        # TODO - check context type
        context = kw.get('context')
        for page_element in context.select(self.selector):
            if cur_page_flag:
                return page_element.get(self.prop)
            if page_element.get(self.prop) == current_link:
                cur_page_flag = True
        raise NextPageNotFoundError


class QueryStringPagination(BasePagination):
    __slots__ = ('param_name', )

    def __init__(self,
                 param_name: str,
                 page_threshold: int = 1,
                 init_page_num: int = 1) -> None:
        super().__init__(page_threshold, init_page_num)
        self.param_name: str = param_name

    def get_next_page(self, current_link: str, **kw: Dict) -> str:
        parsed: ParseResult = parse_url(current_link)
        eqs: str = f'{self.param_name}={self.page}'  # existing query string
        nqs: str = f'{self.param_name}={self.page + 1}'  # new query string
        next_page_url: str = None

        if not parsed.query:
            nqs = f'?{nqs}' if current_link.endswith('/') else f'/?{nqs}'
            next_page_url = current_link + nqs
        elif eqs not in parsed.query:
            next_page_url = current_link + f'&{nqs}'
        else:
            next_page_url = current_link.replace(eqs, nqs)

        self.page += 1

        return next_page_url


class LinkPagination(BasePagination):
    __slots__ = tuple()

    def get_next_page(self, current_link: str, **kw: Dict) -> str:
        self.page += 1
        parsed: ParseResult = parse_url(current_link)

        if parsed.path.endswith(f'/{self.page - 1}'):
            return current_link.replace(f'/{self.page - 1}', f'/{self.page}')
        elif parsed.path.endswith(f'/{self.page - 1}/'):
            return current_link.replace(
                f'/{self.page - 1}/', f'/{self.page}/')
        elif parsed.path.endswith('/'):
            return current_link.replace(
                parsed.path, f'{parsed.path}{self.page}/')
        else:
            return current_link.replace(
                parsed.path, f'{parsed.path}/{self.page}')
