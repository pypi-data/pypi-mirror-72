import os


class Pagination:
    KIND = os.getenv('PAGINATION_KIND', 'kind')
    PROPERTY = os.getenv('PAGINATION_PROPERTY', 'prop')
    SELECTOR = os.getenv('PAGINATION_SELECTOR', 'selector')
    PARAM_NAME = os.getenv('PAGINATION_PARAM_NAME', 'param_name')
    PAGE_THRESHOLD = os.getenv('PAGINATION_PAGE_THRESHOLD', 'page_threshold')

    class Default:
        TYPE = 'dummy'
        PROPERTY = 'href'
        PARAM_NAME = 'page'
        PAGE_THRESHOLD = 50


class PaginationType:
    URL = os.getenv('PAGINATION_TYPE_URL', 'url')
    DUMMY = os.getenv('PAGINATION_TYPE_DUMMY', 'dummy')
    ON_SITE = os.getenv('PAGINATION_TYPE_ON_SITE', 'on_site')
    QUERY_STRING = os.getenv('PAGINATION_TYPE_QUERY_STRING', 'query_string')

