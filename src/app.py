from flask import Flask, render_template, url_for
from flask import redirect


app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login")
def login():
    return render_template("login.html")




if __name__ == "__main__":
    app.run("127.0.0.1",9800,True)