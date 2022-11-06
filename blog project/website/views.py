from curses import flash
#from unicodedata import category
from urllib import request
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Post
from . import db

views = Blueprint("views", "__name__")

@views.route("/")
@views.route("/home")
@login_required

def home():
    return "Home"

@views.route("/about")
def about():
    return render_template("about_me.html")

@views.route("/contact")
def contact():
   return render_template("contact.html")

@views.route("/create_post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        text = request.form.get('text')
        if not text:
            flash('post cannot be blank', category='error')
        else:
            post = Post(text=text, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('post successfully created', category='success')

    return render_template('create_post.html', user=current_user)
