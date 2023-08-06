from .field import Field

from .util import make_bin_op_expression


class BooleanField(Field):
    default_type_name = 'BOOL'

    def __repr__(self):
        return 'Boolean' + super().__repr__()

    @Field.operation
    def __and__(self, other):
        return make_bin_op_expression(self, other, 'AND')

    @Field.operation
    def __or__(self, other):
        return make_bin_op_expression(self, other, 'OR')
