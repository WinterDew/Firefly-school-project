from flask import Flask, render_template, url_for, request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
from models import Users
from bcrypt import hashpw,checkpw

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///firefly.db"
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login/auth",methods=["POST"])
def auth():
    
    print(request.json)
    if Users.query.filter(Users.username == request.json.username).first() != None:
        pass
    return ""

@app.route("/login/signup",methods=["POST"])
def signup():
    return ""

if __name__ == "__main__":
    app.run("127.0.0.1",9800,True)