from coco.pagination.constants import Pagination as PaginationConsts
from coco.pagination.constants import PaginationType
from coco.exceptions import ManifestValidationError
from coco.pagination import interface


class PaginationBuilder:
    metadata = {
        PaginationType.URL: {
            'class': interface.LinkPagination,
            'params': tuple()
        },
        PaginationType.DUMMY: {
            'class': interface.DummyPagination,
            'params': tuple()
        },
        PaginationType.ON_SITE: {
            'class': interface.OnsitePagination,
            'params': (
                PaginationConsts.SELECTOR,
                PaginationConsts.PROPERTY
            )
        },
        PaginationType.QUERY_STRING: {
            'class': interface.QueryStringPagination,
            'params': (PaginationConsts.PARAM_NAME,)
        },
    }

    def __init__(self, spec):
        self.spec = spec

        for param in self.required_params:
            if param not in self.spec or not self.spec[param]:
                raise ManifestValidationError(
                    f'Pagination required attribute {param} is not'
                    f'defined in manifest or has empty value'
                )

    def build(self):
        kwargs = dict()
        parameter_kwarg_map = {
            PaginationConsts.PARAM_NAME: {'param_name': self.param_name},
            PaginationConsts.SELECTOR: {'selector': self.selector},
            PaginationConsts.PROPERTY: {'prop': self.prop}
        }
        for param in self.required_params:
            kwargs.update(parameter_kwarg_map.get(param))

        return self.cls(page_threshold=self.page_threshold, **kwargs)

    @property
    def kind(self):
        return self.spec.get(PaginationConsts.KIND, PaginationType.DUMMY)

    @property
    def selector(self):
        return self.spec.get(PaginationConsts.SELECTOR)

    @property
    def prop(self):
        return self.spec.get(PaginationConsts.PROPERTY)

    @property
    def param_name(self):
        return self.spec.get(PaginationConsts.PARAM_NAME)

    @property
    def page_threshold(self):
        return self.spec.get(
            PaginationConsts.PAGE_THRESHOLD,
            PaginationConsts.Default.PAGE_THRESHOLD
        )

    @property
    def cls(self):
        return self.metadata.get(self.kind).get('class')

    @property
    def required_params(self):
        return self.metadata.get(self.kind).get('params')
