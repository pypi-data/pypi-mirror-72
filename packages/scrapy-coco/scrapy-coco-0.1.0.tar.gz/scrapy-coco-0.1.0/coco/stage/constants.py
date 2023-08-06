import os


class Stage:
    # NOTE - main attributes
    SUB_STAGES = os.getenv('SUB_STAGES', 'subs')
    REQUEST = os.getenv('STAGE_REQUEST', 'request')
    SELECTOR = os.getenv('STAGE_SELECTOR', 'selector')
    # NOTE - delimiters
    NAME_DEL = os.getenv('STAGE_DEL_NAME', 'as')
    ATTR_DEL = os.getenv('STAGE_DEL_ATTR', '::')
    PIPELINE_DEL = os.getenv('STAGE_DEL_PIPELINE', '->')
