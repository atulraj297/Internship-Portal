import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, AdminForm
from flaskblog.models import User, Post, Interested_users
from flask_login import login_user, current_user, logout_user, login_required
import sys


@app.route("/")
@app.route("/home")
def home():
	posts = Post.query.all()
	return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title = 'About')

@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created! You are now able to log in', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Register', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
	
	output_size = (125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)

	return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated!', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', 
		image_file=image_file, form = form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your post has been created!', 'success')
		return redirect(url_for('home'))
	return render_template('create_post.html', title='New Post', 
		form=form,  legend='New Post', user=current_user)

@app.route("/post/<int:post_id>")
def post(post_id):
	post = Post.query.get_or_404(post_id)
	
	users = Interested_users.query.filter_by(post_id=post_id,selected=1).all()
	names = []
	for x in users:
		y = User.query.filter_by(id = x.user_id).first() # y is User
		z = (x.user_id,y.username)
		names.append(z)

	return render_template('post.html', title=post.title, post=post, names = names)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash('Your Post has been updated', 'success')
		return redirect(url_for('post', post_id=post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_post.html', title='Update Post', 
		form=form, legend='Update Post')


@app.route("/post/<int:post_id>/register_for_post", methods=['POST'])
@login_required
def register_for_post(post_id):
	post = Post.query.get_or_404(post_id)
	x = []
	x = Interested_users.query.filter_by(post_id = post_id, user_id = current_user.id).all()
	if len(x) == 0:
		interested_user = Interested_users(post_id = post.id, user_id = current_user.id)
		db.session.add(interested_user)
		db.session.commit()
		flash('Congratulations!!\nYou have successfully registered', 'success')
	else:
		flash('You have already registered for this post', 'success')
	# if post.author != current_user:
	return redirect(url_for('home'))



@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Your Post has been Deleted', 'success')
	return redirect(url_for('home'))


@app.route("/post/<int:post_id>/interested", methods=['GET'])
@login_required
def interested(post_id):
	users = Interested_users.query.filter_by(post_id=post_id).all()
	names = []
	# print("Error in next line:", file=sys.stdout)
	# print(users, file=sys.stdout)
	for x in users:
		y = User.query.filter_by(id = x.user_id).first() # y is User
		flag = Interested_users.query.filter_by(user_id=x.user_id,selected=1).first()
		if flag == None:
			temp = 0
		else:
			q = Interested_users.query.filter_by(user_id=x.user_id,selected=1).all()
			temp = len(q)
		z = (x.user_id,y.username,temp)
		names.append(z)
		#names.append(y.username)
	return render_template('interested.html', names=names, post_id=post_id, users=users)

# for displaying a specific user's public details
@app.route("/user/<int:user_id>", methods=['GET'])
def user(user_id):
	user = User.query.get_or_404(user_id)
	posts = Interested_users.query.filter_by(user_id=user_id,selected=1).all()
	names = []
	for x in posts:
		y = Post.query.filter_by(id=x.post_id).first()
		z = (x.post_id,y.title)
		names.append(z)
	return render_template('user.html', user=user, names=names)

@app.route("/post/<int:post_id>/close", methods=['GET','POST'])
@login_required
def close_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	post.status = 0
	db.session.commit()
	flash('Your Post has been Closed', 'success')
	return redirect(url_for('home'))

@app.route("/post/<int:post_id>/interested/<int:user_id>", methods=['GET','POST'])
@login_required
def interested_select(post_id,user_id):
	print("Here is the field value ---",user_id,post_id)
	users = Interested_users.query.filter_by(post_id=post_id,user_id=user_id).first()
	interested = Interested_users.query.get_or_404(users.id)
	interested.selected = 1
	db.session.commit()
	flash('You have successfully Selected this candidate', 'success')
	#names = []
	# print("Error in next line:", file=sys.stdout)
	# print(users, file=sys.stdout)
	#for x in users:
		#y = User.query.filter_by(id = x.user_id).first() # y is User
		#z = (x.user_id,y.username)
		#names.append(z)
		#names.append(y.username)
	return redirect(url_for('interested', post_id = post_id))
	#return render_template('interested.html', names=names)
	#return redirct(url_for('home'))

@app.route("/admin", methods=['GET', 'POST'])
def admin():
	form = AdminForm()
	if form.validate_on_submit():
		user = User.query.filter_by(id=form.user_id.data).first()
		if user and (form.password.data == 'testing'):
			user.isprof = 1
			db.session.commit()
			flash('Admin Action successful', 'success')
		else:
			flash('Action Unsuccessful. Please check userid and password', 'danger')
	return render_template('admin.html', title='Register', form=form)

'''
	form = AdminForm()
	if form.validate_on_submit():
		user = User.query.get_or_404(form.id)
		user.isprof = 1
		db.session.commit()
		flash('Your post has been created!', 'success')
		return redirect(url_for('home'))
	return render_template('admin.html', title='Admin Section', 
		form=form,  legend='Admin Section', user=current_user)
'''

