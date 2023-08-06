from typing import Iterable, Union, Any, Sized
from .field import Field

from .util import make_func_call_expression


class ArrayField(Field):
    def __init__(self, base_type, **kwargs):
        super().__init__(**kwargs)
        self.base_type = base_type
        self.default_type_name = self.base_type.default_type_name

    def __repr__(self):
        return 'Array' + super().__repr__()[:-1] + f', base_type={self.base_type.__name__})'

    @Field.operation(ftype='boolean')
    def contains(self, items: Union[Iterable, Any]):
        expr = f'EXISTS(SELECT TRUE FROM UNNEST({self.expression}) T WHERE T'
        if isinstance(items, Iterable) and isinstance(items, Sized) and not isinstance(items, str):
            items = tuple(items)
            items = items if len(items) != 1 else f'({repr(items[0])})'
            return f'{expr} IN {items})'

        return f'{expr} = {repr(items)})'

    @Field.operation(ftype='numeric', aggregated=True)
    def len(self):
        return make_func_call_expression('ARRAY_LENGTH', self)
