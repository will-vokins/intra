from flask import Flask
from flask_pymongo import pymongo

CONNECTION_STRING = "censored"

client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('intradb')
users = pymongo.collection.Collection(db, 'users')
