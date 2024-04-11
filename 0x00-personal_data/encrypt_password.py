#!/usr/bin/env python3
"""
0x00. Personal data

encrypt_password  module
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Arguments:
        password(:object:`str`): Password to be hashed

    Return:
        Returns hashed password
    """
    byte_pw = bytes(password, 'utf-8')
    hashee = bcrypt.hashpw(byte_pw, bcrypt.gensalt())
    return hashee


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Arguments:
        hashed_password(:object:`bytes`): Hashed password
        password(:object:`str`): Password whose validity is to be checked

    Return:
        Return true if hashed password corresponds with password. Else false
    """
    byte_pw = bytes(password, 'utf-8')
    return bcrypt.checkpw(byte_pw, hashed_password)
