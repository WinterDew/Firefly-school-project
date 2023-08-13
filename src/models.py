from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Users(db.Model):
    username = db.Column(db.String,primary_key=True)
    password = db.Column(db.String,nullable=False)
    date_joined = db.Column(db.DateTime,default=datetime.utcnow)



