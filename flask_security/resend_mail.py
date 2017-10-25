# coding: utf-8

# -*- coding: utf-8 -*-
"""
    flask_security.resend_email
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Flask-Security recoverable module

    :copyright: (c) 2017 by Timilong(timilong@simright.com).
    :author: xialong Li(timilong@simright.com)
    :license: MIT, see LICENSE for more details.
"""
from flask import current_app as app
from flask import make_response, jsonify

from werkzeug.local import LocalProxy

from .confirmable import generate_confirmation_link
from .utils import do_flash, get_message, send_mail, config_value

# Convenient references
_security = LocalProxy(lambda: app.extensions['security'])

_datastore = LocalProxy(lambda: _security.datastore)


def resend_register_email(user):
    # 当前用户还没有激活 user.confirmed_at->None 提供重发邮件机制
    if not user.confirmed_at:
        confirmation_link, token = generate_confirmation_link(user)
        send_mail(
            config_value('EMAIL_SUBJECT_REGISTER'),
            user.email,
            'welcome',
            user=user,
            confirmation_link=confirmation_link
        )
        return make_response(jsonify(status="0", msg="Resend email success."), 200)
    else:
        return make_response(
            jsonify(
                status="1",
                msg="Your email has been activated. Please don't repeat the operation. "
            )
        )


