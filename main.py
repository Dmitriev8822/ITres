from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config['DEBUG'] = True  # Change at startup !!!
app.config['SECRET_KEY'] = 'my-secret-key'  # NEED CHANGE !!!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'

login_manager = LoginManager(app)
db = SQLAlchemy(app)
app.app_context().push()
