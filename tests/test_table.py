import unittest

from bitable import Table, to_date
from credentials import BASE_ID, BASE_TOKEN

class TestTable(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.table = Table(BASE_ID, BASE_TOKEN, 'api测试表')

    def test_connection(self):
        self.assertEqual(self.table.table_id, 'tblkZOuTOMiMLFKg')

    def test_insert(self):
        self.table.insert({'文本':'Hello', '日期':to_date('2024-07-21'), '单选': 'A', '多选': ['B']})
        self.table.insert([{'文本':'Hello2-1', '日期':to_date('2024-07-21'), '单选': 'A', '多选': ['B']},
                           {'文本':'Hello2-2', '日期':to_date('2024-07-21'), '单选': 'A', '多选': ['B']}])
        
    def test_select(self):
        result = self.table.select({'单选':'X', '多选':['not_in', 'A']})
        self.assertEqual(len(result), 1)
        self.assertEqual(result['文本'], 'Hello')
        


if __name__ == '__main__':
    unittest.main()