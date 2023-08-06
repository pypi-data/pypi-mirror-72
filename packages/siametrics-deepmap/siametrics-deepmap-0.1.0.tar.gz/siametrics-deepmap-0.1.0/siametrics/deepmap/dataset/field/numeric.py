from .field import Field

from .util import make_bin_op_expression, make_func_call_expression


class NumericField(Field):
    default_type_name = 'NUMERIC'

    def __repr__(self):
        return 'Numeric' + super().__repr__()

    @Field.operation(aggregated=True)
    def sum(self):
        return make_func_call_expression('SUM', self)

    @Field.operation(aggregated=True)
    def mean(self):
        return make_func_call_expression('AVG', self)

    @Field.operation(aggregated=True)
    def min(self):
        return make_func_call_expression('MIN', self)

    @Field.operation(aggregated=True)
    def max(self):
        return make_func_call_expression('MAX', self)

    @Field.operation(aggregated=True)
    def std(self):
        return make_func_call_expression('STDDEV', self)

    @Field.operation(aggregated=True)
    def median_approx(self):
        return make_func_call_expression('APPROX_QUANTILES', self, 4) + '[OFFSET(2)]'

    @Field.operation
    def floor(self):
        return make_func_call_expression('FLOOR', self)

    @Field.operation
    def ceil(self):
        return make_func_call_expression('CEIL', self)

    @Field.operation
    def __add__(self, other):
        return make_bin_op_expression(self, other, '+')

    @Field.operation
    def __sub__(self, other):
        return make_bin_op_expression(self, other, '-')

    @Field.operation
    def __mul__(self, other):
        return make_bin_op_expression(self, other, '*')

    @Field.operation
    def __truediv__(self, other):
        return make_func_call_expression('SAFE_DIVIDE', self, other)

    @Field.operation(ftype='boolean')
    def __gt__(self, other):
        return make_bin_op_expression(self, other, '>')

    @Field.operation(ftype='boolean')
    def __ge__(self, other):
        return make_bin_op_expression(self, other, '>=')

    @Field.operation(ftype='boolean')
    def __lt__(self, other):
        return make_bin_op_expression(self, other, '<')

    @Field.operation(ftype='boolean')
    def __le__(self, other):
        return make_bin_op_expression(self, other, '<=')

    @Field.operation(ftype='boolean')
    def __eq__(self, other):
        return make_bin_op_expression(self, other, '==')
