#!/usr/bin/env python3
""" Basic Auth Class module
"""

from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
    Basic Auth Class
    """
    def extract_base64_authorization_header(self, authorization_header:
                                            str) -> str:
        """
        Method that returns the Base64 part of the Authorization
        header for a Basic Authentication:
        """
        if authorization_header is None:
            return None
        elif type(authorization_header) != str:
            return None
        elif not authorization_header.startswith('Basic '):
            return None
        else:
            return authorization_header.split(' ')[-1]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """
        Method that returns the decoded value of a Base64 string
        base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        elif type(base64_authorization_header) != str:
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        Method that returns the user email and password from the Base64 decoded
        value.
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        elif type(decoded_base64_authorization_header) != str:
            return (None, None)
        elif ':' not in decoded_base64_authorization_header:
            return (None, None)
        else:
            return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        """
        Method that returns the User instance based on his email and password.
        """
        if user_email is None or type(user_email) != str:
            return None
        elif user_pwd is None or type(user_pwd) != str:
            return None

        attr = {'email': user_email}
        try:
            users = User.search(attr)

            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        except AttributeError:
            pass

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Method that  overloads Auth and retrieves the User instance for a
        request.
        """
        auth_hdr = self.authorization_header(request)
        b64_aut_hd = self.extract_base64_authorization_header(auth_hdr)
        dec_b64_auth_hdr = self.decode_base64_authorization_header(b64_aut_hd)
        user_cred_tup = self.extract_user_credentials(dec_b64_auth_hdr)

        u_obj = self.user_object_from_credentials(*user_cred_tup)
        return u_obj
