import os


class ModelType:
    HTML = os.getenv('MODEL_TYPE_HTML', 'HTML')
    API = os.getenv('MODEL_TYPE_API', 'API')


class Model:
    NAME = os.getenv('MODEL_NAME', 'name')
    KIND = os.getenv('MODEL_KIND', 'kind')
    STAGES = os.getenv('MODEL_STAGES', 'stages')
    DELAY = os.getenv('DEFAULT_DELAY', 'delay')
    PAGINATION = os.getenv('MODEL_PAGINATION', 'pagination')
    PIPELINE = os.getenv('MODEL_PIPELINE', 'pipeline')
    REQUEST = os.getenv('MODEL_REQUEST', 'request')
    SCHEDULE = os.getenv('MODEL_SCHEDULE', 'schedule')
    PIPELINE_DEL = os.getenv('MODEL_PIPELINE_DEL', '->')

    class Default:
        KIND = os.getenv('MODEL_DEFAULT_KIND', ModelType.HTML)
        DELAY = os.getenv('DEFAULT_DELAY', 0)
