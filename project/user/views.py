"""
    The MIT License (MIT)
    Copyright (c) 2016 Fastboot Mobile LLC.

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# project/user/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask.ext.login import login_user, logout_user, login_required, current_user

from project import bcrypt, db
from project.models import User, PushDevice
from project.user.forms import *
from project.push.tasks import sendpush

import binascii
import os
import json

################
#### config ####
################

user_blueprint = Blueprint('user', __name__,)


################
#### routes ####
################
'''
@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()

        login_user(user)

        flash('Thank you for registering.', 'success')
        return redirect(url_for("user.members"))

    return render_template('user/register.html', form=form)
'''


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None:
            flash("User not found", "danger")
            return render_template('user/login.html', form=form)

        devices = PushDevice.query.filter_by(user_id=user.id).all()

        if len(devices) > 0:
            otp = binascii.b2a_hex(os.urandom(4)).decode()
            user.otp = bcrypt.generate_password_hash(otp)
            print(otp)
            device = devices[0]
            push_status_txt = sendpush(device.push_id, otp)

            push_json = json.loads(push_status_txt)

            if "status" in push_json:
                if push_json['status'] == "OK":
                    flash("One Time Password Sent To Device", "success")
                else :
                    flash("Could Not Communicate With Device", "danger")

            db.session.commit()
            return redirect(url_for('user.two_factor_login'))

        if user and bcrypt.check_password_hash(
                user.password, request.form['password']):
            login_user(user)
            flash('You are logged in. Welcome!', 'success')
            return redirect(url_for('user.members'))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('user/login.html', form=form)
    return render_template('user/login.html', title='Please Login', form=form)


@user_blueprint.route('/2FA', methods=['GET', 'POST'])
def two_factor_login():
    form = TwoFactorLoginForm(request.form)

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if bcrypt.check_password_hash(user.otp, form.otp.data):
                login_user(user)
                flash('You are logged in. Welcome!', 'success')
                user.otp = None
                db.session.commit()
                return redirect(url_for('user.members'))
            else:
                flash('Invalid one time password.', 'danger')
        else:
            flash('Invalid email and/or password.', 'danger')

    return render_template('user/two_factor_login.html', form=form)


@user_blueprint.route('/add_device', methods=['GET', 'POST'])
@login_required
def add_device():
    form = AddDeviceForm(request.form)

    if form.validate_on_submit():
        device = PushDevice.query.filter_by(device_uid=form.device_uid.data).first()

        if device is None:
            flash('Device not found (please check id)', "danger")
        else:
            device.user = current_user
            db.session.commit()
            flash('Device registered to your account', "success")
            return redirect(url_for('user.members'))

    return render_template('user/add_device.html', form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out. Bye!', 'success')
    return redirect(url_for('main.home'))


@user_blueprint.route('/members')
@login_required
def members():

    user = current_user
    devices = PushDevice.query.filter_by(user_id=user.id).all()

    if len(devices) < 1:
        flash('Please <a href="/add_device" class="alert-link">add</a> a two factor auth device', 'info')

    return render_template('user/members.html')
