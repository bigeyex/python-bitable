from .api import Api
from datetime import datetime
from .fieldType import FieldType
from .operator import Conjunction, And, make_filter, wrap_and_filter

class BitableException(Exception):
    pass

OPERATOR_MAP = {
    '==': 'is',
    '!=': 'isNot',
    'empty': 'isEmpty',
    'not_empty': 'isNotEmpty',
    '>': 'isGreater',
    '>=': 'isGreaterEqual', 
    '<': 'isLess',
    '<=': 'isLessEqual',
}

def to_date(date_text):
    d = datetime.strptime(date_text, "%Y-%m-%d")
    return int(d.timestamp() * 1000)


class Table:
    def __init__(self, base_app_token='', token='', table_name='', is_lark=False) -> None:
        self.api = Api(base_app_token, token, is_lark)
        self.table_id = self.api.table_map[table_name]
        table_meta = self.api.get_table_meta(self.table_id)
        self.fields = {field['field_name']: field for field in table_meta}
        

    def select(self, where=None, fields=None, order=None, logic='and') -> list[dict]:
        if where is None:
            raise BitableException('where condition is required')
        
        filter = make_filter(where, self.fields)
        if not isinstance(filter, Conjunction): 
            filter = wrap_and_filter(filter)
        
        sort = []
        for order_item in order:
            if not isinstance(order_item, list):
                sort.append({ "field_name": order_item })
            else: 
                sort.append({ "field_name": order_item[0], "desc": order_item[1] == 'desc' })
        full_result = []
        result = self.api.select_records(self.table_id, filter, fields, sort, logic)
        


    def insert(self, values:None|dict|list[dict]=None):
        if values is None:
            raise BitableException('values are required for insert')
        if not isinstance(values, list):
            values = [values]
        def filter_date_field(insert_value):
            return {k: to_date(v) if self.fields[k]['type'] == FieldType.DateTime.value else v for k, v in insert_value.items()}
        values = [filter_date_field(v) for v in values]
        records = [{'fields': v} for v in values]
        self.api.insert_records(self.table_id, records)
        

    def update(self, values=None, key=None, id=None) -> None:
        pass

    def delete(self, record=None, where=None) -> None:
        pass

    def save(self, record=None) -> None:
        pass
