from crypt import methods
import email
from urllib import request
from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", "__name__")

@auth.route("/login", methods['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user= User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash ('you are logged in', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('incorrect username or password', category='error')
        else:
            flash('email does not exist', category='error')


    return render_template("login.html" )

@auth.route("/signup")
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password= request.form.get('password')

        email_exists= User.query.filter_by(email=email).first()
        user_exists= User.query.filter_by(username=username).first()

        if email_exists:
            flash('email already taken', category='error')
        elif user_exists:
            flash ('username already taken', category='error')
        elif len(username) < 3:
            flash ('username is too short', category='error')
        elif len(email) < 5:
            flash ('email is not valid', category='error')
        elif len(password) <7 :
            flash ('password is too short', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('user created')
            login_user(new_user, remember= True)
            return  redirect(url_for('views.home'))




    return render_template("register.html",  methods['GET', 'POST'])