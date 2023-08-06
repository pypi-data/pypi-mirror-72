def ensure_expression(x):
    from .field import Field

    if isinstance(x, Field):
        return f'{x.expression}'
    return f'{x}'


def make_bin_op_expression(self, other, sign):
    self = ensure_expression(self)
    other = ensure_expression(other)
    expr = f'{self} {sign} {other}'
    return expr


def make_func_call_expression(func, *args):
    args = ', '.join(map(ensure_expression, args))
    return f'{func}({args})'
