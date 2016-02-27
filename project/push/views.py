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

from flask import render_template, Blueprint, request
from project.models import db, PushDevice
import binascii
import os
import json


################
#### config ####
################

push_blueprint = Blueprint('push', __name__,)


################
#### routes ####
################


@push_blueprint.route('/push/register', methods=['POST'])
def register():
    ret_dict = {}

    if 'push_id' in request.form :
        device = PushDevice()
        device.push_id = request.form.get('push_id')
        device.device_uid = binascii.b2a_hex(os.urandom(4)).decode()
        db.session.add(device)
        db.session.commit()

        ret_dict['device_uid'] = device.device_uid

    else :
        ret_dict['error'] = 'could not register push device'

    return json.dumps(ret_dict)


