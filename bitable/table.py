from .api import Api
from datetime import datetime
from .fieldType import FieldType
from .operator import Conjunction, And, make_filter, wrap_and_filter

class BitableException(Exception):
    pass


def to_date(date_text):
    d = datetime.strptime(date_text, "%Y-%m-%d")
    return int(d.timestamp() * 1000)


class Table:
    def __init__(self, base_app_token='', auth_code='', table_name='', table_id=None, is_lark=False):
        self.api = Api(base_app_token, auth_code, is_lark)
        if table_id is not None:
            self.table_id = table_id
        else:
            self.table_id = self.api.table_map[table_name]
        table_meta = self.api.get_table_meta(self.table_id)
        self.fields = {field['field_name']: field for field in table_meta}
        

    def select(self, where=None, fields=None, order=None, limit=None, with_automatic_fields=False):
        
        filter = None
        if where is not None:
            filter = make_filter(where, self.fields)
            if not 'conjunction' in filter: 
                filter = wrap_and_filter(filter)
        
        sort = []
        if order is not None:
            for field in order:
                if isinstance(field, list):
                    sort.append({'field_name': field[0], 'desc': field[1]=='desc'})
                else:
                    sort.append({'field_name': field})
        result = []
        api_result = self.api.select_records(self.table_id, filter, fields, sort, limit, with_automatic_fields)
        for record in api_result:
            item = record['fields']
            for field in item:
                if self.fields[field]['type'] == FieldType.Text.value:
                    text_contents = [text['text'] for text in item[field]]
                    item[field] = ''.join(text_contents)
                elif self.fields[field]['type'] == FieldType.DateTime.value:
                    item[field] = datetime.fromtimestamp(item[field]/1000).strftime("%Y-%m-%d")
            item['_id'] = record['record_id']
            result.append(item)
        return result

    def _filter_date_field(self, record):
        return {k: to_date(v) if k in self.fields and self.fields[k]['type'] == FieldType.DateTime.value else v for k, v in record.items()}

    def insert(self, values=None):
        if values is None:
            raise BitableException('values are required for insert')
        if not isinstance(values, list):
            values = [values]
        values = [self._filter_date_field(v) for v in values]
        records = [{'fields': v} for v in values]
        self.api.insert_records(self.table_id, records)
        

    def update(self, fields=None, where=None) -> None:
        """
            usage:
                update by where condition: 
                    table.update({'FieldMultiple': ['B', 'A'], 'FieldDate':'2024-12-21'}, where={'FieldText': 'HelloTestUpdate'})
                update by save:
                    table.save(record)
        """
        if fields is None:
            raise BitableException('fields are required for update')
        fields = self._filter_date_field(fields)
        if where is not None:
            records = self.select(where, fields=[])
            update_records = [{"fields": fields, "record_id": r['_id']} for r in records]
            self.api.batch_update_records(self.table_id, update_records)
        elif '_id' in fields:
            update_records = [{"fields": {k:v for k,v in fields.items() if k != '_id'}, "record_id": fields['_id']}]
            self.api.batch_update_records(self.table_id, update_records)
        else:
            raise BitableException('provide where condition or a field record with "_id"')
        

    def delete(self, record=None, where=None):
        """
            usage:
                delete by where condition:
                    table.delete(where={'FieldText': 'HelloTestDelete'})
                delete by record:
                    table.delete(record)
        """
        if record is not None:
            if '_id' in record:
                self.api.batch_delete_records(self.table_id, [record['_id']])
            else:
                raise BitableException('record must have "_id" field')
        elif where is not None:
            records = self.select(where, fields=[])
            delete_records = [r['_id'] for r in records]
            self.api.batch_delete_records(self.table_id, delete_records)
        else:
            raise BitableException('provide where condition or a record with "_id"')
