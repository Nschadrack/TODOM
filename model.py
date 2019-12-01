from datetime import datetime
from run import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(50), nullable=False)
	todos = db.relationship('Todo', backref='owner', lazy=True)

	def __repr__(self):
		return"<Users %r %r %r>" % self.username


class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(255), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	date_todo = db.Column(db.DateTime, nullable=False)
	date_completed = db.Column(db.DateTime, nullable=False)
	users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

	def __repr__(self):
		return '<Task %r %r %r %r %r %r >' % (self.id, self.content,self.date_created, self.date_todo, self.date_completed, self.users_id)

