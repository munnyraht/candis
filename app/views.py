from flask import Flask, request
from pymongo import MongoClient
from collections import OrderedDict
import pymongo
from bson import ObjectId
from datetime import datetime
from app import app

client = MongoClient("localhost", 27017)
db = client.invoice


def convert_todate(date_str):
    date_time_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date_time_obj


def convert_toObjectid(id):
    _id = bytes(id[:12], 'utf-8')
    return ObjectId(_id)


# app = Flask(__name__)

# %%timeit
@app.route('/create_invoice', methods=['POST'])
def create_invoice():
    data = request.json

    # convert _id to ObjectId type and save back into the data _id field
    data["_id"] = convert_toObjectid(data["_id"])

    data["contact"]["_id"] = convert_toObjectid(data["contact"]["_id"])

    data['createdAt'] = convert_todate(data['createdAt'])

    data['invoiceDate'] = convert_todate(data['invoiceDate'])

    if data['updatedAt']:
        data['updatedAt'] = convert_todate(data['updatedAt'])

    try:
        db.invoice.insert_one(data)
        # docs = db.invoice.find()
        # for doc in docs:
        #     print(doc)

        return {"message": "invoice created sucessfully"}
    except pymongo.errors.WriteError as e:
        print(e)
        return {"message": "Couldn't update"}


@app.route('/update_contact', methods=['POST'])
def update_contact():
    data = request.json

    # convert _id to ObjectId type and save back into the data _id field
    id = convert_toObjectid(data["_id"])

    filter = {'_id': id}

    # Values to be updated.
    newvalues = {"$set": {'iban': data['iban'],
                          'name': data['name'],
                          'organization': data['organization']}}

    try:
        db.contact.update_one(filter, newvalues)
        return {"message": "invoice updated sucessfully"}
    except Exception as e:
        print(e)
        return {"message": "Couldn't update"}


@app.route('/abnormal_amount', methods=['POST'])
def abnormal_amount():
    data = request.json

    organization = data['organization']
    contactName = data['contactName']
    amount = data['amount']

    docs = db.invoice.find({"organization": organization, "contact.name": {"$regex": "name", "$options": "i"}},
                           {'amount.value': 1, "_id": 0})

    invoices_amount = []
    for doc in docs:
        invoices_amount.append(round(doc['amount']['value']))

    print(invoices_amount)
    if round(amount) in set(invoices_amount):
        response = {"abnormal": False}
    else:
        response = {"abnormal": True}

    return response


