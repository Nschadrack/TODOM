from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin


mainapp = Flask(__name__)
mainapp.config['SECRET_KEY'] = '4ff36fbdf3a2f3bd4fd52ef26b097e3d'
mainapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo_database.db'
db = SQLAlchemy(mainapp)
bcrypt = Bcrypt(mainapp)
login_manager =LoginManager(mainapp)

login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from routes import *

if __name__ == "__main__":

	mainapp.run(debug=True)





