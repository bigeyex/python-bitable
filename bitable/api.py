import requests

class BaseApiException(Exception):
    pass

class Api:
    def __init__(self, base_app_token='', token='', is_lark=False) -> None:
        self.base_app_token = base_app_token
        self.token = token
        self.is_lark = is_lark
        self.table_map = {} # table_name -> table_id
        self.get_tables()
        
    def get_tables(self):
        tables = self.request('/tables/')
        for item in tables['items']:
            self.table_map[item['name']] = item['table_id']

    def get_table_meta(self, table_id):
        meta = self.request(f'/tables/{table_id}/fields')
        return meta['items']
    
    def insert_records(self, table_id, records):
        self.request(f'/tables/{table_id}/records/batch_create', method='POST', 
                     params={}, body={ "records": records })
        
    def select_records(self, table_id, filter, fields=None, sort=None, page_token=None):
        request_body = { "filter": filter, "automatic_fields": True }
        if sort is not None:
            request_body['sort'] = sort
        if fields is not None:
            request_body['field_names'] = fields
        result = []
        data = self.request(f'/tables/{table_id}/records/search', method='POST', 
                     params={}, body=request_body)
        
            
        

    def request(self, path, method='GET', params={'page_size': 100}, body={}):
        headers = {
            'Authorization': f"Bearer {self.token}"
        }
        url_domain = 'https://base-api.feishu.cn' if not self.is_lark else 'https://base-api.larksuite.com'
        url = f'{url_domain}/open-apis/bitable/v1/apps/{self.base_app_token}{path}'
        r = requests.request(method, url, headers=headers, params=params, json=body)
        result = r.json()
        if result['code'] != 0:
            raise BaseApiException(result['msg'])
        return result['data']