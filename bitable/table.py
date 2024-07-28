from .api import Api
from datetime import datetime

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
        # meta = self.api.get_table_meta(self.table_id)
        

    def select(self, where=None, fields=None, order=None, logic='and'):
        if where is None:
            raise BitableException('where condition is required')
        
        conditions = []
        for field_name, cond in where.items():
            if not isinstance(cond, list): 
                conditions.append({ "field_name": field_name, "operator": "is", "value": [cond] })
            else: 
                operator, cond_value = cond
                if operator in OPERATOR_MAP:
                    operator = OPERATOR_MAP[operator]
                if not isinstance(cond_value, list):
                    cond_value = [cond_value]
                conditions.append({ "field_name": field_name, "operator": operator, "value": cond_value })
        sort = []
        for order_item in order:
            if not isinstance(order_item, list):
                sort.append({ "field_name": order_item })
            else: 
                sort.append({ "field_name": order_item[0], "desc": order_item[1] == 'desc' })
        full_result = []
        result = self.api.select_records(self.table_id, conditions, fields, sort, logic)
        


    def insert(self, values=None):
        if values is None:
            raise BitableException('values are required for insert')
        if not isinstance(values, list):
            values = [values]
        records = [{'fields': v} for v in values]
        self.api.insert_records(self.table_id, records)
        

    def update(self, values=None, key=None, id=None):
        pass

    def delete(self, id=None, where=None):
        pass
