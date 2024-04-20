#!/usr/bin/env python3
""" Module of Session views
"""

from api.v1.views import app_views
from os import getenv
from flask import abort, jsonify, request, make_response
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> str:
    """ POST /api/v1/auth_session/login

    Create Session for user
    """
    email = request.form.get('email')
    pwd = request.form.get('password')

    if email is None:
        return jsonify({"error": "email missing"}), 400
    elif pwd is None:
        return jsonify({"error": "password missing"}), 400

    else:
        attr = {'email': email}
        try:
            users = User.search(attr)

            for user in users:
                if user.is_valid_password(pwd):
                    from api.v1.app import auth
                    sess_id = auth.create_session(user.id)

                    resp = make_response(jsonify(user.to_json()))
                    cookie_name = getenv('SESSION_NAME')
                    resp.set_cookie(cookie_name, sess_id)

                    return resp
                else:
                    return jsonify({"error": "wrong password"}), 401
        except (KeyError, AttributeError):
            pass

        return jsonify({"error": "no user found for this email"}), 404


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def session_logout() -> str:
    """DELETE /api/v1/auth_session/logout

    Deletes a user Session
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    else:
        abort(404)
