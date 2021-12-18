from unittest import TestCase
from app import app
import mongomock
import pymongo
from pymongo import MongoClient as PymongoClient
import os
import json

def broken_function():
        raise Exception('This is broken')

class InterfaceTest(TestCase):

    def test__repr(self):
        self.assertEqual(repr(mongomock.MongoClient()),
                         "mongomock.MongoClient('localhost', 27017)")


class DatabaseGettingTest(TestCase):

    def setUp(self):
        super(DatabaseGettingTest, self).setUp()
        self.client = mongomock.MongoClient()

    def test__getting_database_via_getattr(self):
            db1 = self.client.invoice
            self.assertIs(db1, self.client['invoice'])
            self.assertIs(db1.client, self.client)


payload1 = {
        "_id": "unique-invoice-id",
        "organization": "organization-id",
        "createdAt": "2021-10-11T09:53:31.339Z", 
        "updatedAt": "2021-11-29T13:15:19.500Z", 
        "amount": {
        "currencyCode": "EUR",
        "value": 26.3 
        },
        "contact": {
        "_id": "unique-contact-id",
        "iban": "DE88100500001310032358",
        "name": "Contact Name", 
        "organization": "organization-id"
        },
        "invoiceDate": "2021-10-11T00:00:00.000Z", 
        "invoiceId": "VR210230898"
        }

payload2 = {
        "_id": "unique-invoice-id",
        "organization": "organization-id",
        "createdAt": "2021-10-11T09:53:31.000Z", 
        "updatedAt": "2021-11-29T13:15:19.00Z", 
        "amount": {
        "currencyCode": "EUR",
        "value": 26.3 
        },
        "contact": {
        "_id": "unique-contact-id",
        "iban": "DE88100500001310032358",
        "name": "Contact Name", 
        "organization": "organization-id"
        },
        "invoiceDate": "2021-10-11T00:00:00.000Z", 
        "invoiceId": 210230898
        }

payload3 = {
    "_id": "unique-contact-id",
    "iban": "DE88100500001310032358", 
    "name": "Contact Name",
    "organization": "organization-id" 
    }


payload4 = {
    
    "organization": "organization-id",
    "contactName": "partial input or extracted contact name",
    "amount": 1000.0
    }


class candisTests(TestCase):
    # check initial test
    def test_create_invoice_method(self):
        tester = app.test_client(self)
        response = tester.get("/create_invoice")
        self.assertEqual(response.status_code, 405)


    def test_update_contact_method(self):
        tester = app.test_client(self)
        response = tester.get("/update_contact")
        self.assertEqual(response.status_code, 405)


    def test_abnormal_amount_method(self):
        tester = app.test_client(self)
        response = tester.get("/update_contact")
        self.assertEqual(response.status_code, 405)


    def test_create_invoice_insert(self):
        tester = app.test_client(self)
        response = tester.post("/create_invoice", json = payload1)
        message = json.loads(response.data.decode('utf-8'))
        self.assertEqual(message['message'], "Couldn't update")



    def test_create_invoice_insert2(self):
        tester = app.test_client(self)
        # with self.assertRaises(ValueError):
        response = tester.post("/create_invoice", json = payload2)
        message = json.loads(response.data.decode('utf-8'))
        self.assertEqual(message['message'], "Couldn't update")


    def test_update_contact(self):
        tester = app.test_client(self)
        response = tester.post("/update_contact", json = payload3)
        message = json.loads(response.data.decode('utf-8'))
        self.assertEqual(message['message'], "invoice updated sucessfully")


    def test_abnormal_amount(self):
        tester = app.test_client(self)
        # with self.assertRaises(KeyError):
        response = tester.post("/abnormal_amount", json = payload4)
        message = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(message['abnormal'])


if __name__ == "__main__":
    unittest.main()
