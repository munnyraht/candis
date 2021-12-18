
from pymongo import MongoClient
from collections import OrderedDict
import pymongo

client = MongoClient("localhost", 27017)
db = client.invoice

try:
    db.create_collection("invoice")   
except pymongo.errors.CollectionInvalid as e:
    pass

try:
    db.create_collection("contact")   
except pymongo.errors.CollectionInvalid as e:
    pass


# add schema
organization_schema =    { "$jsonSchema": {
              "bsonType": "object",
              "required": [ "_id", "organization", "createdAt", "amount", "invoiceDate", "invoiceId"],
              "properties": {
                "_id": {
                    "bsonType": "objectId",
                    "description": "must be a objectId and is required"
                 },
                 "organization": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                 },
                 "createdAt": {
                    "bsonType": "date",
                    "description": "must be a date"
                 },
                 "updatedAt": {
                    "bsonType": "date",
                    "description": "must be a date if the field exists"
                 },
                 "amount": {
                   "bsonType": "object",
                   "required": [ "currencyCode", "value" ],
                   "properties": {
                        "currencyCode" : {
                            "bsonType": "string",
                            "description": "must be a string and is required"
                            },
                        "value": {
                            "bsonType": "double",
                            "minimum" :0,
                            "description": "must be a double and is required"
                            }
                       }},

                 "invoiceDate":{
                    "bsonType": "date",
                    "description": "must be a date and is required"
                        },

                "invoiceId":{
                    "bsonType": "string",
                    "description": "must be a string and is required"
                        },

                 }
              }
           }

contact_schema = { "$jsonSchema": {
                  "bsonType": "object",
                  "required": [ "_id","iban","name","organization"],
                  "properties": {
                    "_id": {
                        "bsonType": "objectId",
                        "description": "must be a objectId and is required"
                     },
                     "iban": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                     },
                     "name": {
                        "bsonType": "string",
                        "description": "must be a date"
                     },
                     "organization": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                     },
                        }
               } }


cmd = OrderedDict([('collMod', 'invoice'),
            ('validator', organization_schema),
            ('validationLevel', 'moderate')])

cmd_ = OrderedDict([('collMod', 'contact'),
            ('validator', contact_schema),
            ('validationLevel', 'moderate')])
    
db.command(cmd)
db.command(cmd_)