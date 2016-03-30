from flask import (render_template, redirect, request, url_for, flash,
        current_app)
from flask.ext.login import (login_user, logout_user, login_required, 
        current_user)
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegistrationForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User.query.filter_by(username=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.homepage'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.homepage'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    # Disable registration if necessary
    if request.method == 'POST' and not current_app.config.get('ALLOW_REGISTRATION'):
        flash('Registration has been disabled. Try again another time.')

        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        current_app.logger.warn('User attempting to register: {}'.format(ip))
        return redirect(url_for('main.homepage'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                username=form.username.data,
                password=form.password.data)
        db.session.add(user)
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    else:
        return render_template('auth/register.html', form=form)


@auth.before_app_request
def touch():
    if current_user.is_authenticated:
        user = db.session.query(User).\
                filter(User.id == current_user.get_id()).\
                first()
        user.ping()
        current_app.logger.debug('Pinged user: {}'.format(user.username))
        db.session.add(user)

