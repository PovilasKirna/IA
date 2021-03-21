from .forms import LoginForm, RegistrationForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from ..users.utils import elligible, save_picture, send_reset_email, notify_admin_about_new_user
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User
from .. import db

users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in!')
        return redirect(url_for('main.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                if user.registered:
                    flash('Logged in successfully!', category='success')
                    if user.role == 'Admin':
                        return redirect(url_for('admin.index'))
                    return redirect(url_for('main.home'))
                else:
                    return redirect(url_for('users.registered'))
            else:
                flash('Incorect user details!', category='error')
        else:
            flash('User doen\'t exist!', category='error')
            
    return render_template('login.html', user=current_user, form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users.route('/signup', methods=['GET', 'POST'])
@users.route('/register', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        flash('You are already registered in!')
        return redirect(url_for('main.home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data, 
            password=generate_password_hash(form.password.data, method='sha256'),
            phone=form.phone.data
        )
        db.session.add(new_user)
        db.session.commit()
        admin = User.query.filter_by(role='Admin').first()
        notify_admin_about_new_user(new_user, admin)
        flash('Account created successfully!', category ='success')
        login_user(new_user)
        return redirect(url_for('users.registered'))  
    
    return render_template('register.html', user=current_user, form=form)

@users.route('/user', methods=['GET', 'POST'])
@login_required
@elligible(current_user)
def user():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile_picture = picture_file
        current_user.name = form.name.data
        current_user.surname = form.surname.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Your account has been updated!', category='success')
        return redirect(url_for('users.user'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.surname.data = current_user.surname
        form.email.data = current_user.email
        form.phone.data = current_user.phone
    profile_picture = url_for('static', filename='images/profile_pictures/'+ current_user.profile_picture)
    return render_template('UserProfile.html', user=current_user, profile_picture=profile_picture, form=form)
    
    
@users.route('/registered')
@login_required
def registered():
    if current_user.registered:
        flash('You are already registered.')
        return redirect(url_for('main.home'))
    return render_template('registered.html', user=current_user)

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', category='info')
        return redirect(url_for('users.login'))
    
    return render_template('reset_request.html', form=form, user=current_user)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user= User.verify_reset_token(token)
    if not user:
        flash('That token is invalid or expired', category='warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password=generate_password_hash(form.password.data, method='sha256'),
        user.password = password
        db.session.commit()
        flash('Your password has been updated!', category ='success')
        return redirect(url_for('users.login'))  
         
    return render_template('reset_token.html', form=form, user=current_user)
