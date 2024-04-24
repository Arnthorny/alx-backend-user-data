#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User
from typing import TypeVar, Dict


class DB:
    """DB class
    """
    ATTRIBS = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> TypeVar('User'):
        """
        The method, which has two required string arguments: email and
        hashed_password, and returns a User object. The method should save the
        user to the database

        Arguments:
            email(`str`): The user's email.
            hashed_password(`str`): The user's password
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs: Dict) -> TypeVar('User'):
        """
        This method takes in arbitrary keyword arguments and returns the first
        row found in the users table as filtered by the method’s input
        argument.
        """
        list_of_queries = []
        for item in kwargs.items():
            if item[0] not in self.ATTRIBS:
                raise InvalidRequestError
            tmp_str = '{}=:{}'.format(item[0], item[0])
            list_of_queries.append(tmp_str)

        q_str = ' OR '.join(list_of_queries)
        user = self._session.query(User).filter(
            text(q_str)).params(**kwargs).first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs: Dict) -> None:
        """
        This method that takes as argument a required user_id integer and
        arbitrary keyword arguments, and returns None.

        Args:
            user_id(`int`): Id of user to be updated
        """
        user = self.find_user_by(id=user_id)

        for item in kwargs.items():
            if item[0] not in self.ATTRIBS:
                raise ValueError
            setattr(user, item[0], item[1])

        self._session.commit()
