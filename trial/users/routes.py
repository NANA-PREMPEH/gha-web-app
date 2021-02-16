from flask import render_template, redirect, url_for, flash, request, Blueprint
from werkzeug.urls import url_parse
from flask_login import current_user, logout_user, login_required, login_user
from trial import db, bcrypt 
from trial.users.forms import RequestResetForm, ResetPasswordForm, LoginForm, UpdateAccountForm
from trial.users.utils import send_reset_email, save_picture
from trial.models import User, Post
import boto3
users = Blueprint('users', __name__) 


#Route for Login 
@users.route('/login', methods=['GET', 'POST']) 
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        #Get User from Database
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data): 
            login_user(user, remember=form.remember.data)
            
            #Get the next parameter(if it exists redirect the user the requested page)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.home')
            return redirect(next_page)

        else:
            flash('Unsuccessful Login. Please check email and password again', 'danger')
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('users/login.html', title='Login', form=form, posts=posts) 

#route for account template
@users.route('/account', methods=['GET', 'POST']) 
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit(): 
        #Check if there is a picture data
        if form.picture.data:
            #Set the user profile picture 
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        #Set Updated details in the database
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit() 
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    #Populate fields with data from the database
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
   
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('users/account.html', title='Account', form=form, image_file=image_file, posts=posts)


#Route for logout
@users.route('/logout')
def logout():
    logout_user() 
    return redirect(url_for('users.login'))

#Route to request reset Password(Where Email is entered to reset password)
@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() 
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('users/reset_request.html', title='Reset Password', form=form, posts=posts)

#Route for Reset Password
@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token) 
    if user is None: 
        flash('Token is invalid or expired', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        #Hash Password
        hashed_pswd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #Edit the password in the database
        user.password = hashed_pswd
        db.session.commit()
        flash('Password has been updated successfully!. You can now log in', 'success')
        return redirect(url_for('users.login'))
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('users/reset_token.html', title='Reset Password', form=form, posts=posts)  
