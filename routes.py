from flask import render_template, request, url_for, redirect,flash
from model import *
from run import mainapp,bcrypt
from form import*
from flask_login import login_user, current_user, logout_user,login_required


@mainapp.route("/")
def index():
	return render_template("index.html")


@mainapp.route("/home", methods=['POST', 'GET'])
@login_required
def home():
	if request.method =='POST':
		task_content = request.form.get('content')
		date_todo_task_form = request.form.get('date_todo_task')
		date_task_completed_form = request.form.get('date_task_completed')
		
		my_date_todo = datetime.strptime(date_todo_task_form, "%Y-%m-%d")

		my_date_completed = datetime.strptime(date_task_completed_form, '%Y-%m-%d')

		new_task = Todo(content=task_content, date_todo=my_date_todo, date_completed=my_date_completed, owner=current_user)
		if not task_content or not my_date_todo or not my_date_completed:
			return redirect("/home")
		else:
			db.session.add(new_task)
			db.session.commit()
			return redirect("/home")
	else:
		found = 0
		tasks = Todo.query.order_by(Todo.date_created).all()
		for task in tasks:
			if task.owner.username == current_user.username:
				found=found+1
		return render_template("home.html", tasks=tasks, found=found)



@mainapp.route("/delete/<int:id>")
def delete(id):
	task_to_delete = Todo.query.get_or_404(id)

	if task_to_delete:
		db.session.delete(task_to_delete)
		db.session.commit()
		return redirect("/home")

	else:
		return"There was A problem to delete the task"

@mainapp.route("/update/<int:id>", methods=["GET","POST"])
def update(id):
	task_to_update = Todo.query.get_or_404(id)

	if request.method =="POST":

		task_content = request.form.get('content')
		date_todo_task_form = request.form.get('date_todo_task')
		date_task_completed_form = request.form.get('date_task_completed')

		my_date_todo = datetime.strptime(date_todo_task_form, "%Y-%m-%d")
		my_date_completed = datetime.strptime(date_task_completed_form, '%Y-%m-%d')

		task_to_update.content =  task_content
		task_to_update.my_date_todo =  my_date_todo
		task_to_update.my_date_completed =  my_date_completed

		if not task_content or not my_date_todo or not my_date_completed:
			return"problem to update your task"
		else:
			db.session.commit()
			return redirect("/home")
			
	else:
		return render_template("update.html", task=task_to_update)



@mainapp.route("/register", methods=["POST", "GET"])
def register():
	form = RegistrationForm()
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = Users(username=form.username.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Account created, now you are able to login', 'success')
		return redirect(url_for('login'))
	return render_template("register.html", form=form)


@mainapp.route("/login", methods=["POST", "GET"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(username=form.username.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next_page')
			flash('Login successfully', 'success')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login unsuccesfully, check password and username', 'danger')
	return render_template("login.html", form=form)

	
@mainapp.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))