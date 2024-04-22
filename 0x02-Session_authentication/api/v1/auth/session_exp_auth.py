#!/usr/bin/env python3
"""
Session Exp Auth Module
"""

from api.v1.auth.session_auth import SessionAuth
from models.user import User
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    This class defines a session expiration object
    """
    def __init__(self):
        try:
            self.session_duration = int(getenv('SESSION_DURATION', 0))
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Overloaded function for create_session
        """
        sess_id = super().create_session(user_id)
        if sess_id is None:
            return None
        sess_dict = {'user_id': user_id, 'created_at': datetime.now()}
        self.user_id_by_session_id[sess_id] = sess_dict
        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """
        Overloaded function for user_id_for_session_id
        """
        if session_id is None:
            return None

        sess_dict = self.user_id_by_session_id.get(session_id)
        if sess_dict is None:
            return None
        if self.session_duration <= 0:
            return sess_dict.get('user_id')
        elif sess_dict.get('created_at') is None:
            return None

        time_elapsed = timedelta(seconds=self.session_duration) +\
            sess_dict.get('created_at')
        if time_elapsed < datetime.now():
            return None
        else:
            sess_dict.get('user_id')
