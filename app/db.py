from flask import Flask
from flask_pymongo import pymongo

CONNECTION_STRING = "mongodb+srv://application:bd464443316fcbd3b07ce651e16358a4@cluster0.fzjuy.mongodb.net/intradb?retryWrites=true&w=majority"

client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('intradb')
users = pymongo.collection.Collection(db, 'users')