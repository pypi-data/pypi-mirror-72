from typing import Iterable, Tuple
import pandas as pd
import numpy as np

from .field import NumericField, StringField, ArrayField, BooleanField, Field, ensure_expression


def make_select_clause(fields):
    select = []
    for field in fields:
        select.append(field.get_select_query())
    if not select:
        raise ValueError('No variables to be selected.')

    select = ', '.join(select)
    return select


def parse_fields_dict(s, dataset):
    fields = {}

    for d in s:
        name = d['name']
        type_ = d['type']
        expression = d.get('expression', d['name'])
        aggregated = d.get('aggregated', False)

        if type_ in ('INTEGER', 'FLOAT'):
            ftype = NumericField
        elif type_ in ('STRING',):
            ftype = StringField
        else:
            raise NotImplementedError(f'field type {d["type"]} is not implemented.')

        if d.get('repeated', False):
            field = ArrayField(name=name, expression=expression, type_name=type_,
                               base_type=ftype, aggregated=aggregated, dataset=dataset)
        else:
            field = ftype(name=name, expression=expression, type_name=type_,
                          aggregated=aggregated, dataset=dataset)

        fields[name] = field

    return fields


class Dataset:
    def __init__(self, source, client, fields=None, fields_dict=None, conditions=None):
        self.source = source

        self._fields = fields or parse_fields_dict(fields_dict, self)
        for field in self._fields.values():
            field.dataset = self

        self.client = client
        self.conditions = conditions or []

    @property
    def project_id(self):
        return self.client.project_id

    @property
    def columns(self):
        return tuple(self._fields.keys())

    @property
    def schema(self):
        schema = []
        for name, field in self._fields.items():
            record = {
                'name': name,
                'type': field.type_name,
                'repeated': isinstance(field, ArrayField),
                'description': field.description,
            }
            schema.append(record)

        return pd.DataFrame(schema).set_index('name')

    def get_query(self):
        query = 'SELECT '

        select = make_select_clause(self._fields.values())
        query += select + f' FROM {self.source}'

        if self.conditions:
            query += self.get_where_clause()

        return query

    def __getitem__(self, key):
        if isinstance(key, str):
            return self._fields[key]

        elif isinstance(key, Iterable):
            fields = {}
            for k in key:
                if isinstance(k, Field):
                    fields[k.name] = k
                elif isinstance(k, str):
                    fields[k] = self._fields[k]
                else:
                    raise NotImplementedError()

            dataset = Dataset(self.source, self.client, fields=fields, conditions=self.conditions)
            return dataset
        elif isinstance(key, BooleanField) and not key.aggregated:
            conditions = self.conditions + [key.expression]
            dataset = Dataset(self.source, self.client, fields=self._fields, conditions=conditions)
            return dataset
        else:
            raise NotImplementedError()

    def get(self):
        query = self.get_query()
        return self.client.query(query)

    def __setitem__(self, key, value):
        assert isinstance(key, str)

        if isinstance(value, Field):
            value = value.rename(key)
        elif isinstance(value, bool):
            BooleanField(key, value, type_name='BOOLEAN', dataset=self)
        elif isinstance(value, (int, float, np.number)):
            NumericField(key, value, type_name='NUMERIC', dataset=self)
        elif isinstance(value, str):
            StringField(key, value, type_name='STRING', dataset=self)
        else:
            raise NotImplementedError('constant field of type {type(value)} is not implemented.')

        self._fields[key] = value

    def drop(self, columns, inplace=False, errors='raise'):
        assert errors in ('raise', 'ignore')

        columns = columns if isinstance(columns, Iterable) and not isinstance(columns, str) else [columns]

        if errors == 'raise':
            my_columns = set(self.columns)
            assert all(isinstance(c, str) and c in my_columns for c in columns)

        fields = {k: v for k, v in self._fields.items() if k not in columns}

        if inplace:
            self._fields = fields
        else:
            dataset = Dataset(self.source, self.client, fields=fields, conditions=self.conditions)
            return dataset

    def __delitem__(self, key):
        self.drop(key, inplace=True)

    def get_base_query(self):
        return f'({self.get_query()})'

    def get_where_clause(self):
        where = ''
        if self.conditions:
            where = ' WHERE ' + ' AND '.join([f'{c}' for c in self.conditions])
        return where

    def groupby(self, keys, *fields: Field):
        fields = list(fields)

        assert all(isinstance(field, Field) and field.aggregated for field in fields)

        keys = [key if isinstance(key, Field) else self._fields[key] for key in keys]

        select = make_select_clause(keys + fields)
        from_ = self.get_base_query()
        groupby = ', '.join(map(str, range(1, len(keys)+1)))
        where = self.get_where_clause()

        source = f'(SELECT {select} FROM {from_}{where} GROUP BY {groupby})'

        fields = {field.name: field.copy() for field in keys + fields}
        for field in fields.values():
            field.expression = field.name

        dataset = Dataset(source, client=self.client, fields=fields)
        return dataset

    def agg(self, *fields: Field):
        assert all(field.aggregated for field in fields)

        select = make_select_clause(fields)
        from_ = self.get_base_query()
        where = self.get_where_clause()

        query = f'SELECT {select} FROM {from_}{where}'
        return self.client.query(query)
