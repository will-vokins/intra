import db
import forms

from flask import Flask, render_template, flash, redirect, url_for
from flask_pymongo import PyMongo
from forms import RegistrationForm
from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['version'] = 'Alpha 2'
app.config['SECRET_KEY'] = '06428f29a279cddf7fac4b0180db9579'

@app.route('/')
def root():
    return render_template("root.html", app=app), 200

@app.route('/login')
def login():
    return render_template("login.html"), 200

@app.route('/register', methods=["GET", "POST"])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created successfully, you may now log in.')
        db.db.users.insert_one({"username": form.username.data, "email": form.email.data, "password": bcrypt.generate_password_hash(form.password.data).decode('utf-8' )})
        return redirect(url_for('login'))
    return render_template("register.html", form=form), 200