from typing import Dict, List, Any
from collections import defaultdict
import pandas as pd
from google.cloud import bigquery

from .dataset import Dataset


class Parameter:
    def __init__(self, name, required, description, type_, template, arbitrary=False):
        self.name = name
        self.required = required
        self.description = description
        self.type_ = type_

        self.template = template
        self.arbitrary = arbitrary

    @classmethod
    def from_param_dict(cls, param):
        return cls(name=param['name'], required=param['required'],
                   description=param['description'], type_=param['type'], template=param['template'],
                   arbitrary=param.get('arbitrary', False))

    def modify_query(self, query, value):
        if 'where' in self.template:
            if self.type_.endswith('[]'):
                if self.arbitrary:
                    clause = self.template['where'].format(*value)
                else:
                    value = tuple(value) if len(value) != 1 else f'({repr(value[0])})'
                    clause = self.template['where'].format(value)
            else:
                clause = self.template['where'].format(value)

            query['where'].append(clause)
        else:
            raise NotImplementedError('Other template types are not implemented.')

        return query

    def __repr__(self):
        required = ' REQUIRED' if self.required else ''
        description = self.description[:50] + ('...' if len(self.description) > 50 else '')

        return f'dataset.Parameter(<{self.type_}>{self.name}{required}; {description})'


class SourceDataset(Dataset):
    def __init__(self, name, metadata, client):
        self.__gbq_table = self.__load_gbq_table(client, name)

        fields_dict = self.__load_fields_dict()  # type: List[Dict[str, Any]]

        super().__init__(source=name, client=client, fields_dict=fields_dict)

        self.__params = [Parameter.from_param_dict(param) for param in metadata['params']]

        assert metadata['query']['source'].lower() == 'bigquery'
        self.table = metadata['query']['params']['table']

        self.__num_rows = None
        self.__num_bytes = None
        self.__description = None

    def __load_fields_dict(self):
        table = self.__gbq_table

        fields_dict = []
        for s in table.schema:
            record = {
                'name': s.name,
                'type': s.field_type,
                'repeated': s.mode == 'REPEATED',
                'description': s.description,
            }
            fields_dict.append(record)

        return fields_dict

    def __get_stats(self):
        select = []
        for name, s in self.schema.iterrows():
            if not s.repeated:
                select.append(f'MIN({s.name}) AS {s.name}__min')
                select.append(f'MAX({s.name}) AS {s.name}__max')
            select.append(f'COUNT({s.name}) AS {s.name}__count')
        query = 'SELECT ' + ', '.join(select) + f' FROM {self.table}'

        stats = self.client.query(query)

        aggs = defaultdict(dict)

        for key, value in stats.iloc[0].to_dict().items():
            name, agg = key.split('__')
            aggs[name][agg] = value

        stats = pd.DataFrame(aggs).T.sort_index(axis=1)
        return stats

    def __load_description(self):
        stats = self.__get_stats()
        description = pd.concat([self.schema, stats], axis=1, sort=True)
        self.__description = description

    @staticmethod
    def __load_gbq_table(dm_client, table):
        scopes = ['https://www.googleapis.com/auth/bigquery.readonly']
        cred = dm_client.get_credentials(scopes)
        client = bigquery.Client(credentials=cred, project=dm_client.project_id)

        dataset_id, table_id = table.split('.')
        dataset_ref = client.get_dataset(f'{dm_client.project_id}.{dataset_id}')
        table_ref = dataset_ref.table(table_id)
        table = client.get_table(table_ref)

        return table

    def __load_details(self):
        table = self.__gbq_table
        self.__num_rows = table.num_rows
        self.__num_bytes = table.num_bytes

    @property
    def params(self):
        params = []
        for param in self.__params:
            record = {
                'name': param.name,
                'type': param.type_,
                'description': param.description,
            }
            params.append(record)
        return pd.DataFrame(params)

    @property
    def num_rows(self):
        if not self.__num_rows:
            self.__load_details()
        return self.__num_rows

    @property
    def num_bytes(self):
        if not self.__num_bytes:
            self.__load_details()
        return self.__num_bytes

    @property
    def description(self):
        if self.__description is None:
            self.__load_description()

        return self.__description

    def __get_query(self, fields, **kwargs):
        query = {
            'table': self.table,
            'where': [],
        }

        for param in self.__params:
            name = param.name
            if name in kwargs:
                query = param.modify_query(query, kwargs[name])
            elif param.required:
                raise ValueError(f'Please provide required parameters: {param.name}')

        where_clause = ' AND '.join(query['where'])
        fields_string = ', '.join(fields)
        query_string = f"SELECT {fields_string} FROM {query['table']} WHERE {where_clause}"

        return query_string

    def fetch(self, fields=None, **kwargs):
        fields = fields or ['*']
        query = self.__get_query(fields, **kwargs)
        df = self.client.query(query)
        return df

    def get_base_query(self):
        return self.source
