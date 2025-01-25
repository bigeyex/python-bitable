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
        
    def batch_update_records(self, table_id, records):
        """
            record format: {"fields": {...}, "record_id": "..."}
            doc: https://open.larkoffice.com/document/server-docs/docs/bitable-v1/app-table-record/batch_update
        """
        self.request(f'/tables/{table_id}/records/batch_update', method='POST',
                     params={}, body={ "records": records })
        
    def batch_delete_records(self, table_id, record_ids):
        self.request(f'/tables/{table_id}/records/batch_delete', method='POST',
                     params={}, body={ "records": record_ids })
        
    def select_records(self, table_id, filter, fields=None, sort=None, limit=None, with_automatic_fields=False):
        request_body = { "filter": filter, "automatic_fields": True }
        if sort is not None:
            request_body['sort'] = sort
        if fields is not None:
            request_body['field_names'] = fields
        if with_automatic_fields:
            request_body['automatic_fields'] = True
        result = []
        
        has_more = True
        page_token = None
        page_size = limit if limit is not None and limit <= 500 else 500

        while has_more:
            params = {'page_size': page_size}
            if page_token is not None:
                params['page_token'] = page_token
            records = self.request(f'/tables/{table_id}/records/search', method='POST', 
                     params=params, body=request_body)
            result.extend(records['items'])
            if 'page_token' in records:
                page_token = records['page_token']
                if limit is not None:
                    limit -= page_size
                    if limit <= 0:
                        break
                    page_size = limit if limit <= 500 else 500
            else:
                has_more = False
        return result
            
        

    def request(self, path, method='GET', params={'page_size': 100}, body={}):
        headers = {
            'Authorization': f"Bearer {self.token}"
        }
        url_domain = 'https://base-api.feishu.cn' if not self.is_lark else 'https://base-api.larksuite.com'
        url = f'{url_domain}/open-apis/bitable/v1/apps/{self.base_app_token}{path}'
        r = requests.request(method, url, headers=headers, params=params, json=body)
        result = r.json()
        if result['code'] != 0:
            raise BaseApiException(f"{result['code']}: {result['msg']}")
        return result['data']