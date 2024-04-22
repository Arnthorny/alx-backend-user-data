#!/usr/bin/env python3
"""
Session Db Auth Module
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from os import getenv
from datetime import datetime, timedelta, timezone


class SessionDBAuth(SessionExpAuth):
    """
    This class defines a session db object
    """
    def create_session(self, user_id=None):
        """
        Overloaded function that creates and stores new instance of UserSession
        and returns the Session ID
        """
        if user_id is None:
            return None

        sess_id = super().create_session(user_id)
        u_session = UserSession(user_id=user_id, session_id=sess_id)
        u_session.save()
        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """
        Overloaded function that returns the User ID by requesting UserSession
        in the database based on session_id
        """
        if session_id is None:
            return None
        attr = {'session_id': session_id}
        try:
            sess_obj = UserSession.search(attr)[0]
            if self.session_duration <= 0:
                return sess_obj.user_id
            elif sess_obj.created_at is None:
                return None

            time_elapsed = timedelta(seconds=self.session_duration) +\
                sess_obj.created_at
            if time_elapsed <= datetime.utcnow():
                return None
            else:
                return sess_obj.user_id

        except (KeyError, AttributeError, IndexError):
            return None

    def destroy_session(self, request=None):
        """
        Overloaded function that destroys the UserSession based on the Session
        ID from the request cookie
        """
        if request is None:
            return False
        sess_id = self.session_cookie(request)
        if sess_id is None:
            return False

        attr = {'session_id': sess_id}
        try:
            sess_obj = UserSession.search(attr)[0]
            sess_obj.remove()
            return True
        except (KeyError, AttributeError, IndexError):
            return False
