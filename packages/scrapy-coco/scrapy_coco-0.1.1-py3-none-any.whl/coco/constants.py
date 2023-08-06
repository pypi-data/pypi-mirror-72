import os


class Const:
    NA = os.getenv('CONST_NA', 'N/A')
    TEXT = os.getenv('CONST_TEXT', 'text')
    HTML = os.getenv('CONST_HTML', 'html')


class Request:
    KEY = os.getenv('REQUEST_KEY_NAME', 'key')
    LINKS = os.getenv('REQUEST_LINK', 'links')
    DATA = os.getenv('REQUEST_DATA', 'data')
    METHOD = os.getenv('REQUEST_METHOD', 'method')
    TIMEOUT = os.getenv('REQUEST_TIMEOUT', 'timeout')
    HEADERS = os.getenv('REQUEST_HEADERS', 'headers')
    COOKIES = os.getenv('REQUEST_COOKIES', 'cookies')

    class Default:
        METHOD = 'GET'
        TIMEOUT = 3000
