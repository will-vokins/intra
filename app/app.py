import db
import forms

from flask import Flask, render_template, flash, redirect, url_for, request, session
from flask_pymongo import PyMongo
from forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['version'] = 'Alpha 3'
app.config['SECRET_KEY'] = '06428f29a279cddf7fac4b0180db9579' # INSECURE - DO NOT USE IN PRODUCTION

@app.route('/')
def root():
    return render_template("root.html", app=app), 200

@app.route('/app')
def dashboard():
    if 'username' in session:
        return render_template("dashboard.html"), 200
    return redirect('login')

@app.route('/login', methods=["GET", "POST"])
def login():

    form = LoginForm()
    if request.method =="POST":

        # Query for document containing username in collection
        users = db.db.users
        login_user = users.find_one({'username': request.form['username']})

        # If query returns a document, check that the passwords match
        if login_user:
            if bcrypt.check_password_hash(login_user['password'], request.form['password']):
                session['username'] = request.form['username']
                # Interrupt process and redirect to dashboard
                return redirect(url_for('dashboard'))
            else:
                flash('Password incorrect', 'error')
        else:
            flash('User does not exist', 'error')
    
    return render_template("login.html", form=form), 200
        

@app.route('/register', methods=["GET", "POST"])
def registration():
    
    form = RegistrationForm()
    formErrors = 0

    if request.method == 'POST':

        if form.validate_on_submit():
            
            # Check if username is already registered
            Query = { "username": form.username.data }
            if db.db.users.find(Query).count() > 0:
                
                # Flag errors to prevent processing of form, set error flash
                formErrors = formErrors + 1
                flash('Sorry, that username is unavailable', 'error')

            # Check if email is already registered
            Query = { "email": form.email.data }
            if db.db.users.find(Query).count() > 0:

                #Flag errors to prevent processing of form, set error flash
                formErrors = formErrors + 1
                flash('That email address is already associated with another account.', 'error')
            
            # If any error flags are present, return client to registration() with error flashes
            if formErrors != 0:
                return render_template("register.html", form=form), 200

            # If no error flags are present, insert document > `users` collection, set success flash, redirect to dashboard()
            db.db.users.insert_one({"username": form.username.data,
                                    "email": form.email.data,
                                    "password": bcrypt.generate_password_hash(form.password.data).decode('utf-8' )})
            
            flash('✔ Account created successfully, you may now log in.', 'success')
            session['username'] =  form.username.data
            return redirect(url_for('dashboard'))

    # Render the registration page if no form data is received
    return render_template("register.html", form=form), 200