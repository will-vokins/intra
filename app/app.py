# Author:   Will Vokins
# Contact:  will.vokins@outlook.com
# This is private code, no licensing is provided.

# IMPORTS
import db
import forms
import cloudinary as Cloud
import secrets
import base64
import re

# FROM
from flask import Flask, render_template, flash, redirect, url_for, request, session
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from forms import RegistrationForm, LoginForm, ClientSetupForm

# APP CONFIGURATION
app = Flask(__name__)
app.config['version'] = 'Alpha 3'
app.config['URL'] = 'http://localhost:5000/'
app.config['SECRET_KEY'] = '06428f29a279cddf7fac4b0180db9579' # INSECURE - DO NOT USE IN PRODUCTION
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'vokinsw@gmail.com',
    MAIL_PASSWORD = 'censored'
)

# INITS
bcrypt = Bcrypt(app)
mail = Mail(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', code=404), 404

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
                session['username'] = login_user['username']
                session['avatar'] = login_user['avatar']

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
                                    "password": bcrypt.generate_password_hash(form.password.data).decode('utf-8' ),
                                    "avatar": "/static/img/defaultAvatar.png"})
            
            flash('✔ Account created successfully, you may now log in.', 'success')
            session['username'] =  form.username.data
            session['avatar'] = "/static/img/defaultAvatar.png"
            return redirect(url_for('dashboard'))

    # Render the registration page if no form data is received
    for error in form.password.errors:
        flash(error, 'error')
    return render_template("register.html", form=form), 200

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('root'))


@app.route('/user')
def profile():
    return render_template("profile.html")

@app.route('/clients')
def clients():
    return render_template("clients/clients.html")

@app.route('/clients/new', methods=["POST"])
def newClient():
    if 'username' in session:
        if request.method == 'POST':
            
            # Collect email from request, check that it is a valid email address
            email = request.form.get('email')
            regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            if not (re.search(regex,email)):
                return("Invalid email address given."), 590

            # Check if client is already assigned to current user
            Query = { "email": email, "user": session['username'] }
            if db.db.invites.find(Query).count() > 0:
                return("Failure: Invite already exists."), 400
            
            # Insert client and current session user into invites collection
            generated_key = secrets.token_hex(16)
            db.db.invites.insert_one({"email": email,
                                    "user": session['username'],
                                    "key": generated_key})

            # Send email to client, requesting account setup (clientSetup())
            msg = Message(session['username'] + ' wants to collaborate!', sender = 'vokinsw@gmail.com', recipients = [email])
            msg.html = "<h1>You've been Invited</h1><p>" + session['username'] + " has invited you to collaborate.</p><p>Don't worry, getting started takes less than 30 seconds.</p><p>Visit the link below to begin.</p><p>" + app.config['URL'] + session['username'] + "/" + generated_key
            mail.send(msg)
            return("Success: " + email), 200
        else:
            return("Unauthorized"), 401
                        
    return("Failure: Unauthorized"), 401
    
@app.route('/<user>')
def clientDashboard(user):

    # Check that user exists
    userQuery = db.db.users.find_one({"username": user})
    if userQuery == None:
        # If user does not exist, return 404
        return render_template("error.html", code=404), 404

    # If user does exist, return user 
    return(user)

@app.route('/<user>/<key>', methods=["GET", "POST"])
def clientSetup(user, key):

    form = ClientSetupForm()

    # Check if user exists
    userQuery = db.db.users.find_one({"username": user,})
    if userQuery == None:
        # If user does not exists, return 404
        return render_template("error.html", code=404), 404

    # Check if the user->client invite key is valid and belongs to the correct user
    invite = db.db.invites.find_one({"user": user, 
                                     "key": key})
    if invite == None:
        # If key isn't valid, return expired key content
        return ("<center><h1>Invalid or expired key</h1></center>")
    
    # If key and user are valid:
    if request.method == "POST":
        if form.validate_on_submit():
            print(user + "VALIDATED FORM")
            db.db.clients.insert_one({"email": invite['email'],
                                      "user": user,
                                      "password": bcrypt.generate_password_hash(form.password.data).decode('utf-8' ),
                                      "avatar": "/static/img/defaultAvatar.png"})
            deletion = db.db.invites.delete_one({"user": user, "key": key})

    return render_template("/clients/client_setup.html", user=userQuery, key=user, invite=invite, form=form)

# if `py app.py` -> debug=True
if __name__ == '__main__':
    app.run(debug=True)
