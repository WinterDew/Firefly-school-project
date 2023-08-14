from flask import Flask, render_template, url_for, request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
from bcrypt import hashpw,checkpw,gensalt
from flask_migrate import Migrate


app = Flask(__name__)


@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login/auth",methods=["POST"])
def auth():
    
    print(request.json)
    return ""

@app.route("/login/signup",methods=["POST"])
def signup():
    return ""

if __name__ == "__main__":
    app.run("127.0.0.1",9800,True)