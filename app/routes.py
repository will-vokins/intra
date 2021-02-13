from __main__ import app

@app.route('/')
def root():
    return render_template("root.html", app=app), 200

@app.route('/login')
def login():
    return render_template("login.html"), 200

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

            # If no error flags are present, insert document > `users` collection, set success flash, redirect to login
            db.db.users.insert_one({"username": form.username.data,
                                    "email": form.email.data,
                                    "password": bcrypt.generate_password_hash(form.password.data).decode('utf-8' )})
            
            flash('✔ Account created successfully, you may now log in.', 'success')
            return redirect(url_for('login'))

    return render_template("register.html", form=form), 200