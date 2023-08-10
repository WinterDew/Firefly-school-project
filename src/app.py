from flask import Flask, render_template
from flask import redirect

app = Flask(__name__)

@app.route("/")
def index():
    return None

@app.route("/login")
def login():
    return render_template("login.html")




if __name__ == "__main__":
    app.run("127.0.0.1",9800,True)