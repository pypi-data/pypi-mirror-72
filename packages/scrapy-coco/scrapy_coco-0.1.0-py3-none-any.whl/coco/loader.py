import inspect
import logging
from importlib import import_module

LOG = logging.getLogger('coco')


def load_pipeline(pipeline_function: str):
    """
    [Built in pipeline definitions]
        - native_link
    [User defined pipeline definitions]
        - fancy_cow
    """

    module = None
    function = None
    pipeline_modules = ('coco.pipelines', 'pipelines')

    for pipeline_module in pipeline_modules:
        try:
            module = import_module(pipeline_module)
            function = getattr(module, pipeline_function)
        except (ModuleNotFoundError, AttributeError):
            pass

    if not function:
        raise AttributeError(
            f'Pipeline "{str(pipeline_function)}" not found in pipeline '
            f'modules: {str(pipeline_modules)}',
        )
    if not inspect.isfunction(function):
        raise TypeError(f'Pipeline function {function} must be callable')
    if not inspect.iscoroutinefunction(function):
        raise TypeError(f'Pipeline function {function} must be async')

    if not inspect.signature(function).parameters:
        # TODO - not true for stage pipeline
        raise TypeError((
            f'Pipeline function {function} must except 2 parameters: ',
            f'model[Model] and items[List]'
        ))

    return function
