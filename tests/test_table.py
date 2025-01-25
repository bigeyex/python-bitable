import unittest

from bitable import Table, And, Greater, Or, Contain
from credentials import BASE_ID, BASE_TOKEN


class TestTable(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.table = Table(BASE_ID, BASE_TOKEN, 'api测试表')

    def test_connection(self):
        self.assertEqual(self.table.table_id, 'tblkZOuTOMiMLFKg')

    def test_insert_delete(self):
        # insert 3 records
        self.table.insert({'FieldText':'HelloDelete', 'FieldDate':'2024-12-21', 'FieldSingle': 'A', 'FieldMultiple': ['B']})
        self.table.insert([{'FieldText':'HelloDelete', 'FieldDate':'2024-12-22', 'FieldSingle': 'A', 'FieldMultiple': ['B']},
                           {'FieldText':'HelloDelete', 'FieldDate':'2024-12-23', 'FieldSingle': 'A', 'FieldMultiple': ['B']}])
        results = self.table.select({'FieldText': 'HelloDelete'})
        self.assertEqual(len(results), 3)

        # delete 1 by object
        self.table.delete(results[0])
        results = self.table.select({'FieldText': 'HelloDelete'})
        self.assertEqual(len(results), 2)
        
        # delete 2 by where
        self.table.delete(where={'FieldText': 'HelloDelete'})
        results = self.table.select({'FieldText': 'HelloDelete'})
        self.assertEqual(len(results), 0)
        
    def test_update(self):
        # update by where condition
        self.table.update({'FieldMultiple': ['B', 'A'], 'FieldDate':'2024-12-21'}, where={'FieldText': 'HelloTestUpdate'})
        result = self.table.select({'FieldText': 'HelloTestUpdate'})[0]
        self.assertEqual(len(result['FieldMultiple']), 2)
        self.assertEqual(result['FieldDate'], '2024-12-21')

        # update by save
        result['FieldMultiple'] = ['B']
        result['FieldDate'] = '2024-12-22'
        self.table.update(result)
        result = self.table.select({'FieldText': 'HelloTestUpdate'})[0]
        self.assertEqual(len(result['FieldMultiple']), 1)

    def test_select(self):
        # plain select
        records = self.table.select({'FieldText': 'HelloTestSelect'})[0]
        self.assertEqual(records['FieldSingle'], 'X')
        self.assertEqual(records['FieldDate'], '2024-07-22')

        # select with operator
        records = self.table.select(Greater('FieldValue', 90))
        self.assertEqual(len(records), 1)
        
        # select with conjunction
        records = self.table.select(Or(Greater('FieldValue', 90), And({'FieldSingle': 'A'}, Contain('FieldText', 'TestSelect2'))))
        self.assertEqual(len(records), 2)
        


if __name__ == '__main__':
    unittest.main()