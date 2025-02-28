from flask import render_template, flash, redirect, request, url_for
from urllib.parse import urlparse
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, MadeCourseForm
from app.models import User, Course



@app.route('/')
@app.route('/index')
@login_required
def index():
    courses = db.session.query(Course).all()
    # posts = [
    #     {
    #         'author': {'username': 'John'},
    #         'body': 'Beautiful day in Portland!'
    #     },
    #     {
    #         'author': {'username': 'Susan'},
    #         'body': 'The Avengers movie was so cool!'
    #     }
    # ]
    return render_template('index.html', title='Home', course=courses)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html',  title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/courses', methods=['GET', 'POST'])
def courses():
    form = MadeCourseForm()
    if form.validate_on_submit():
        course = Course(namecourse=form.namecourse.data)
        db.session.add(course)
        db.session.commit()
        flash('Congratulations, you are now make a course!')
        # flash('Login requested for user {}, remember_me={}'.format(
        #     form.namecourse.data, form.madecourse.data))
        return redirect(url_for('index'))
    return render_template('courses.html',  title='Courses', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
