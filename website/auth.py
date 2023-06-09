from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
import re

auth = Blueprint('auth', __name__)


@auth.route("/login", methods = ['GET', 'POST'])
def login():
    """checks if user exists - give access to get in to his account and perform more operations"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email = email).first()
        if user and correct_password(user, password):
            return redirect(url_for('views.home'))
        else:
            flash("user dosn\'t exists", category = "error")
            return redirect(url_for('auth.sign_up'))
    else:
        return render_template("login.html", user = current_user)


def correct_password(user, password):
    """when user exists, check if he entered a correct password with a security hash"""
    if check_password_hash(user.password, password):
        flash("logged in successfully", category = 'success')
        # saves current logged user info
        login_user(user, remember = True)
        return True
    else:
        flash("incorrect password, try again", category = 'error')
        return False


@auth.route("/logout")
@login_required
def logout():
    """logout for current user and redirect to login page.
        works only when ther is someone logged in"""
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods = ['GET', 'POST'])
def sign_up():
    """responsible for the sign-up page
        if POST-get information , check user dosent exists (other-ways redirect to log-in page)
        if all data is valid adds user to DB and remember this user as the logged in user,
        then, current_user keeps info about the current logged user"""
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email = email).first()
        if user:
            flash("email already exists", category = 'error')
            return redirect(url_for('auth.login'))
        if len(email) < 4:
            flash("email must be longer then 3 characters", category = 'error')
        elif not is_valid(email):
            flash("email is not valid", category = 'error')
        elif len(first_name) < 2:
            flash("firstname must be greater then 1 characters", category = 'error')
        elif password1 != password2:
            flash("password do\'t match", category = 'error')
        elif len(password1) < 7:
            flash("password must be at least 7  characters", category = 'error')
        else:
            new_user = User(email = email, first_name = first_name,
                            password = generate_password_hash(password1, method = 'sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember = True)
            flash("Account created", category = 'success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user = current_user)


def is_valid(email):
    """test email validation with regex"""
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
        return True
    else:
        return False
