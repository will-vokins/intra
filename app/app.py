from flask import Flask, render_template
app = Flask(__name__)
app.config["version"] = "Alpha 1"

@app.route('/')
def root():
    return render_template("root.html", app=app), 200

@app.route('/login')
def login():
    return render_template("login.html"), 200