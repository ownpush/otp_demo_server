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

# project/main/views.py


#################
#### imports ####
#################

from flask import render_template, Blueprint, request, flash
from project.main.forms import SendToDeviceForm
from project.models import PushDevice
from project.push.tasks import sendpush
import binascii
import os
import json


################
#### config ####
################

main_blueprint = Blueprint('main', __name__,)


################
#### routes ####
################


@main_blueprint.route('/', methods=['GET', 'POST'])
def home():
    form = SendToDeviceForm(request.form)

    if form.validate_on_submit():
        device = PushDevice.query.filter_by(device_uid=form.device_uid.data).first()

        if device is None:
            flash('Device not found (please check id)', "danger")
        else:
            otp = binascii.b2a_hex(os.urandom(4)).decode()
            push_status_txt = sendpush(device.push_id, otp)
            push_json = json.loads(push_status_txt)

            if "status" in push_json:
                if push_json['status'] == "OK":
                    flash("One Time Password Sent To Device", "success")
                else:
                    flash("Could Not Communicate With Device ( " + push_status_txt + " )", "danger")

    return render_template('main/home.html', form=form)


@main_blueprint.route("/about/")
def about():
    return render_template("main/about.html")
