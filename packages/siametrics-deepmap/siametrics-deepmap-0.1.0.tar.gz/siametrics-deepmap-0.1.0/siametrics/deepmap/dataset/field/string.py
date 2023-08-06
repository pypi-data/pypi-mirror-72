from .field import Field

from .util import make_func_call_expression


class StringField(Field):
    default_type_name = 'STRING'

    def __repr__(self):
        return 'String' + super().__repr__()

    @Field.operation
    def upper(self):
        return make_func_call_expression('UPPER', self)

    @Field.operation
    def lower(self):
        return make_func_call_expression('LOWER', self)

    @Field.operation(ftype='numeric')
    def len(self):
        return make_func_call_expression('LENGTH', self)

    @Field.operation(ftype='boolean')
    def contains(self, substring):
        return ' '.join([self.expression, 'LIKE', f'"%{substring}%"'])

    @Field.operation(ftype='boolean')
    def startswith(self, substring):
        return ' '.join([self.expression, 'LIKE', f'"{substring}%"'])

    @Field.operation(ftype='boolean')
    def endswith(self, substring):
        return ' '.join([self.expression, 'LIKE', f'"%{substring}"'])
