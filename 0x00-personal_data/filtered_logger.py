#!/usr/bin/env python3
"""
0x00. Personal data

filtered_logger  module
"""

from typing import List, Sequence, Union, Tuple
import re
import logging
import mysql.connector
import os

PII_FIELDS = ('email', 'phone', 'ssn', 'password', 'name')


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    A function called filter_datum that returns
    the log message obfuscated

    Arguments:
        fields(:object:`list`): List of strings representing
        all fields to obfuscate

        redaction(:object:`str`): a string representing by what the field
        will be obfuscated

        message(:object:`str`): a string representing the log line

        separator(:object:`str`): a string representing by which character is
        separating all fields in the log line (message)

    Return:
        (:object: `str`): The log message obfuscated
    """
    rpl = '{0}={1}{2}'
    for fld in fields:
        message = re.sub("{0}=.*?{1}".format(fld, separator),
                         rpl.format(fld, redaction, separator), message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class

    Arguments:
        fields(:object:`list`): List of strings representing
        all fields to obfuscate

    Attributes:
        REDACTION(:object:`str`): a string representing by what the field
        will be obfuscated

        FORMAT(:object:`str`): a string representing the format of logs

        SEPARATOR(:object:`str`): a string representing by which character is
        separating all fields in the log line (message)
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        self.flds = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Method to filter values in incoming log records using filter_datu"""
        msg = record.getMessage()
        # record.__dict__['msg'] = new_msg
        new_msg = super(RedactingFormatter, self).format(record)
        return filter_datum(self.flds, self.REDACTION, new_msg, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    A function that takes no arguments and returns a logging.Logger object.
    logger is named "user_data" at a "logging.INFO" level
    """

    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    stream_handl = logging.StreamHandler()
    r_formatter = RedactingFormatter(PII_FIELDS)

    stream_handl.setFormatter(r_formatter)
    logger.propagate = False
    logger.addHandler(stream_handl)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Function that returns a connector to the database
    """
    arg_keys = ('user', 'password', 'host', 'database')
    arg_vals = (os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
                os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
                os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
                os.getenv('PERSONAL_DATA_DB_NAME', ''))

    conn_params = dict(zip(arg_keys, arg_vals))
    conn = mysql.connector.connect(**conn_params)
    return conn


def main() -> None:
    """
    Function to start the logging from db
    """
    db = get_db()
    logger = get_logger()

    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    heading = cursor.column_names

    for row in cursor:
        rowDict = dict(zip(heading, row))
        # print(rowDict)
        msg = '; '.join('='.join((str(key), str(val))) for (key, val) in
                        rowDict.items()) + ';'
        logger.info(msg)
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
