#!/usr/bin/env python3
"""
Session Auth Module
"""

from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """
    This class defines a session authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        This method creates a Session ID for a user_id
        """
        if type(user_id) != str:
            return None
        else:
            new_sess_id = str(uuid4())
            self.user_id_by_session_id[new_sess_id] = user_id
            return new_sess_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        This method returns a User ID based on a Session ID
        """
        if type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        This method returns a User instance based on a cookie value
        """
        sess_cookie = self.session_cookie(request)
        u_id = self.user_id_for_session_id(sess_cookie)

        return User.get(u_id)

    def destroy_session(self, request=None):
        """
        Method that deletes the user session / logout
        """
        if request is None:
            return False
        sess_id = self.session_cookie(request)
        if sess_id is None:
            return False

        u_id = self.user_id_for_session_id(sess_id)
        if u_id is None:
            return False

        self.user_id_by_session_id.pop(sess_id, None)
        return True
