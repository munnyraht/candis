from unittest import TestCase
from db import db
import mongomock

class InterfaceTest(TestCase):

    def test__repr(self):
        self.assertEqual(repr(mongomock.MongoClient()),
                         "mongomock.MongoClient('localhost', 27017)")



class DatabaseGettingTest(TestCase):

    def setUp(self):
        super(DatabaseGettingTest, self).setUp()
        self.client = mongomock.MongoClient()

#     def test__getting_database_via_getattr(self):
#             db1 = self.client.invoice
#             self.assertIs(db1, self.client['invoice'])
#             self.assertIs(db1.client, self.client)
           


