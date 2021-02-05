from flask import Flask, render_template, flash, redirect 
from flask_pymongo import PyMongo

import db
import forms

app = Flask(__name__)
app.config['version'] = 'Alpha 1'
app.config['SECRET_KEY'] = '06428f29a279cddf7fac4b0180db9579'

@app.route('/')
def root():
    return render_template("root.html", app=app), 200

@app.route('/login')
def login():
    return render_template("login.html"), 200

@app.route('/register')
def register():
    return render_template("register.html"), 200