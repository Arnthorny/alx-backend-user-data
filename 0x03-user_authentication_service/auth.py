#!/usr/bin/env python3
"""
Auth Module
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union, TypeVar
from user import User


def _hash_password(password: str) -> bytes:
    """
    This method takes in a password string arguments and returns bytes.
    The returned bytes is a salted hash of the input password, hashed with
    bcrypt.hashpw.
    """
    p_bytes = bytes(password, 'utf-8')
    p_hash = bcrypt.hashpw(p_bytes, bcrypt.gensalt())
    return p_hash


def _generate_uuid() -> str:
    """
    Return a string representation of a new UUID
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        This method should take mandatory email and password string arguments
        and return a User object.

        Args:
            email(`str`): The user's email.
            password(`str`): The user's password.

        Description:
            If a user already exist with the passed email, raise a ValueError
            with the message User <user's email> already exists.
            If not, hash the password with _hash_password, save the user to the
            database using self._db and return the User object
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            h_pwd = _hash_password(password)
            user = self._db.add_user(email, h_pwd)
            return user
        else:
            raise ValueError('User {} already exists'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """
        This method should validate a user's email and password.

        Args:
            email(`str`): The user's email.
            password(`str`): The user's password.

        Returns:
            bool: True if valid else false
        """
        if type(email) != str or type(password) != str:
            return False
        try:
            user = self._db.find_user_by(email=email)
            b_pwd = bytes(password, 'utf-8')
            if bcrypt.checkpw(b_pwd, user.hashed_password):
                return True
        except NoResultFound:
            pass
        return False

    def create_session(self, email: str) -> Union[str, None]:
        """
        This method takes an email string argument and returns the session ID
        as a string

        Args:
            email(`str`): The user's email.

        Returns:
            (`str`): Session ID
        """
        try:
            user = self._db.find_user_by(email=email)
            sess_id = _generate_uuid()
            self._db.update_user(user.id, session_id=sess_id)

            return sess_id
        except NoResultFound:
            pass
        return None

    def get_user_from_session_id(self, session_id: str) ->\
            Union[User, None]:
        """
        This method takes a single session_id string argument and returns the
        corresponding User or None.
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            pass
        return None

    def destroy_session(self, user_id: str) -> None:
        """
        This method takes a single user_id integer argument and returns None.
        The method updates the corresponding user’s session ID to None.
        """
        try:
            user = self._db.update_user(user_id, session_id=None)
        except (NoResultFound, ValueError):
            pass
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        This method takes an email string argument and returns a string.

        Find the user corresponding to the email. If the user does not exist,
        raise a ValueError exception. If it exists, generate a UUID and update
        the user’s reset_token database field. Return the token.
        """
        try:
            token = _generate_uuid()
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        else:
            self._db.update_user(user.id, reset_token=token)
            return token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        This method takes reset_token string argument and a password string
        argument and returns None.

        Use the reset_token to find the corresponding user. If it does not
        exist, raise a ValueError exception.

        Otherwise, hash the password and update the user’s hashed_password
        field with the new hashed password and the reset_token field to None.
        """
        if reset_token is None or password is None:
            raise ValueError
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        else:
            h_pwd = _hash_password(password)
            self._db.update_user(user.id, hashed_password=h_pwd)
            self._db.update_user(user.id, reset_token=None)
