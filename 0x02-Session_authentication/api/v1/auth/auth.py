#!/usr/bin/env python3
""" Auth Class module
"""

from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """
    THis contains functions for
    authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns False for now
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        elif path in excluded_paths or f'{path}/' in excluded_paths:
            return False

        for e_path in excluded_paths:
            if e_path.endswith('*'):
                e_path_prefix = e_path[:-1]
                if path.startswith(e_path_prefix):
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns none for now
        """
        if request is None:
            return None
        elif request.headers.get('Authorization') is None:
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns None for now
        """
        return None

    def session_cookie(self, request=None):
        """
        Method that returns a cookie value from a request:
        """
        cookie_name = getenv('SESSION_NAME')
        if request is None:
            return None
        return request.cookies.get(cookie_name)
