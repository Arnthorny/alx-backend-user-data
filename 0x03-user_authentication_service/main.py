#!/usr/bin/env python3
"""
Create a new module called main.py. Create one function for each of the
following tasks. Use the requests module to query your web server for the
corresponding end-point. Use assert to validate the response’s expected status
code and payload (if any) for each task.
"""
import requests


def register_user(email: str, password: str) -> None:
    """
    Function to test user registration

    Args:
        email(`str`): An email address
        password(`str`): User password
    """
    data = {'email': email, 'password': password}
    r = requests.post('http://localhost:5000/users', data=data)

    res_json = r.json()
    exp_res = {"email": email, "message": "user created"}

    assert(res_json == exp_res)
    assert(r.status_code == 200)


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Function to test wrong pwd login
    """
    data = {'email': email, 'password': password}
    r = requests.post('http://localhost:5000/sessions', data=data)

    assert(r.status_code == 401)


def log_in(email: str, password: str) -> str:
    """
    Function to test login details
    """
    data = {'email': email, 'password': password}
    r = requests.post('http://localhost:5000/sessions', data=data)

    res_json = r.json()
    exp_res = {"email": email, "message": "logged in"}

    assert(res_json == exp_res)
    assert(r.status_code == 200)

    return r.cookies['session_id']


def profile_unlogged() -> None:
    """
    Function to attempt to access the profile without a log in
    """
    r = requests.get('http://localhost:5000/profile')

    assert(r.status_code == 403)


def profile_logged(session_id: str) -> None:
    """
    Function to to access the profile while logged in
    """
    cookies = {'session_id': session_id}
    r = requests.get('http://localhost:5000/profile', cookies=cookies)

    res_json = r.json()
    exp_res = {"email": EMAIL}

    assert(res_json == exp_res)
    assert(r.status_code == 200)


def log_out(session_id: str) -> None:
    """
    Function to simulate a lofout
    """
    cookies = {'session_id': session_id}
    r = requests.delete('http://localhost:5000/sessions', cookies=cookies)

    res_json = r.json()
    exp_res = {"message": "Bienvenue"}

    assert(res_json == exp_res)
    assert(r.status_code == 200)


def reset_password_token(email: str) -> str:
    """
    Function to reset user password
    """
    data = {'email': email}
    r = requests.post('http://localhost:5000/reset_password', data=data)

    res_json = r.json()
    exp_res = {'email': email, 'reset_token': res_json['reset_token']}

    assert(exp_res == res_json)
    assert(r.status_code == 200)

    return res_json['reset_token']


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Function to update user password
    """
    data = {'email': email, 'reset_token': reset_token,
            'new_password': new_password}
    r = requests.put('http://localhost:5000/reset_password', data=data)

    res_json = r.json()
    exp_res = {"email": email, "message": "Password updated"}

    assert(exp_res == res_json)
    assert(r.status_code == 200)


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
