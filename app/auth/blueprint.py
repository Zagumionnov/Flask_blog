from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from auth.forms import LoginForm, SignupForm
from models import User

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Incorrect credential')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        return redirect(url_for('posts.profile'))

    form = LoginForm()
    return render_template('auth/login.html', form=form)


@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        # repeat_password = request.form['repeat_password']

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists')
            return redirect(url_for('auth.signup'))

        try:
            new_user = User(
                name=name,
                email=email,
                password=generate_password_hash(password, method='sha256')
            )
            db.session.add(new_user)
            db.session.commit()
        except:
            print('Smth wrong')

    form = SignupForm()
    return render_template('auth/signup.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('posts.index'))
