#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask, jsonify, request, abort, make_response, redirect
from flask import Response
from flask import url_for
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def root() -> Response:
    """Root route
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> Response:
    """Endpoint to register user
    FORM body:
      - email
      - password
    Return:
      - Confirmation JSON message
      - 400 if user already exists
    """
    rj = {'email': request.form.get('email'), 'password':
          request.form.get('password')}
    try:
        new_user = AUTH.register_user(**rj)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    ret_msg = {"email": new_user.email, "message": "user created"}
    return jsonify(ret_msg)


@app.route('/sessions', methods=['POST'])
def login() -> Response:
    """Endpoint to log user in
    Form body:
      - email
      - password
    Return:
      - Confirmation JSON message
      - 401 if info is incorrect
    """
    rj = {'email': request.form.get('email'), 'password':
          request.form.get('password')}

    if (AUTH.valid_login(*rj.values())):
        res_msg = {"email": rj['email'], "message": "logged in"}
        resp = make_response(jsonify(res_msg))

        cookie_name = 'session_id'
        cookie_val = AUTH.create_session(rj['email'])
        resp.set_cookie(cookie_name, cookie_val)

        return resp
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout() -> Response:
    """Endpoint to logout

    Deletes a user session
    """
    cookie_name = 'session_id'
    sess_id = request.cookies.get(cookie_name)
    if sess_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(sess_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for('root'))


@app.route('/profile')
def profile() -> Response:
    """Endpoint to profile

    Get a user profile.
    """
    cookie_name = 'session_id'
    sess_id = request.cookies.get(cookie_name)
    if sess_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(sess_id)
    if user is None:
        abort(403)
    else:
        return jsonify({"email": user.email})


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> Response:
    """Endpoint to reset user password
    """
    email = request.form.get('email')
    if email is None:
        abort(403)
    try:
        tok = AUTH.get_reset_password_token(email)
        res = {"email": email, "reset_token": tok}

        return jsonify(res)
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password() -> Response:
    """Endpoint to update user password
    """
    rj = {'reset_token': request.form.get('reset_token'),
          'new_password': request.form.get('new_password')}

    try:
        AUTH.update_password(*rj.values())
        email = request.form.get('email')

        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
