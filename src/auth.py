from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db
# from .models import User  # Assume you have a User model

auth = Blueprint('auth', __name__)

@auth.route('/student-login',methods=['POST'])
def student_login():
    ...
    return



"""

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Your login logic here

    return "Login page"


@auth.route('/register', methods=['GET', 'POST'])
def register():
    # Your registration logic here
    return "Register page"
@auth.route('/logout')
def logout():
    # Your logout logic here

    flash('You have been logged out.', 'success')
    return redirect(url_for('views.home'))
"""