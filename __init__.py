from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager

app= Flask(__name__)
app.secret_key = "adidasadsdasfasfa"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost/hoteldb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True

db= SQLAlchemy(app=app)
admin = Admin(app=app, name="HOTEL MANAGEMENT",template_mode="bootstrap4")
login = LoginManager(app=app)

