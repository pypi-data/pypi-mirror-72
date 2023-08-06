from functools import wraps

from .util import make_func_call_expression


def _operation(func_=None, ftype=None, aggregated=False):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, name=None, **kwargs):
            from siametrics.deepmap.dataset.field.ref import str_field_mapper

            func_name = func.__name__.strip('_')
            name = name or f'{self.name}__{func_name}'
            ftype_ = ftype or self.__class__
            if isinstance(ftype_, str):
                ftype_ = str_field_mapper[ftype_]

            expr = '(' + func(self, *args, **kwargs) + ')'
            result = ftype_(name, expr, type_name=ftype_.default_type_name, dataset=self.dataset,
                            aggregated=aggregated)

            return result

        return wrapper

    if func_ is None:
        return decorator
    return decorator(func_)


class Field:
    default_type_name = 'ANY'

    operation = staticmethod(_operation)

    def __init__(self, name, expression, type_name, dataset=None, description=None, aggregated=False):
        self.name = name
        self.expression = expression
        self.type_name = type_name
        self.dataset = dataset
        self.description = description or ''
        self.aggregated = aggregated

    def copy(self):
        field = self.__class__(self.name, self.expression, self.type_name, self.dataset,
                               self.description, self.aggregated)
        return field

    def get_select_query(self):
        return f'{self.expression} AS {self.name}'

    def rename(self, name):
        return self.__class__(name, self.expression, type_name=self.type_name, dataset=self.dataset,
                              description=self.description, aggregated=self.aggregated)

    def __repr__(self):
        return f'Field({repr(self.name)})'

    @_operation(ftype='numeric', aggregated=True)
    def count(self):
        return make_func_call_expression('COUNT', self)

    @_operation(ftype='numeric', aggregated=True)
    def nunique(self):
        return make_func_call_expression('COUNT', f'DISTINCT {self.expression}')


Field_operation = Field.operation
