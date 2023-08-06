from siametrics.deepmap.dataset.field import NumericField, ArrayField, StringField, BooleanField

str_field_mapper = {
    'numeric': NumericField,
    'array': ArrayField,
    'string': StringField,
    'boolean': BooleanField,
}