#!/usr/bin/env python3
"""
Module that contains definition of class User
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    """
    This class inherits from Base and links to the MySQL table `users`

    Attributes:
    id(int): The integer primary key.
    email(str): A non-nullable string
    hashed_password(str): A non-nullable string
    session_id(str): A nullable string
    reset_token(str): A nullable string
    """
    __tablename__ = 'users'

    id = Column('id', Integer, primary_key=True, autoincrement=True)

    email = Column('email', String(250), nullable=False)

    hashed_password = Column('hashed_password', String(250), nullable=False)

    session_id = Column('session_id', String(250), nullable=True)

    reset_token = Column('reset_token', String(250), nullable=True)
