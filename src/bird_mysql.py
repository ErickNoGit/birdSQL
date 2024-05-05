# Python 3.12.3
import os
import sys
import json
import mysql.connector
from os import PathLike
from pathlib import Path
from typing import Union
from mysql.connector.cursor_cext import CMySQLCursor 
from mysql.connector.connection_cext import CMySQLConnection

src = os.path.dirname(Path(__file__))
sys.path.append(src)

from bird import BirdSystem


class BirdMySQL(BirdSystem):
    """Responsible for all functions linked to MySQL"""

    def __init__(self) -> None:
        """Loads basic connection data"""
        super().__init__()
        self.__CLASS_NAME = str(self.__class__.__name__)

        self.__BASE_CONECT = {
            'host': None,
            'user': None,
            'pass_': None,
            'data_base': None
        }

        self.__debug_conn = None
        self.__conn = None
        self.__cursor_ = None


    def conn_mysql(self, con: Union[PathLike, dict] = None, **kwargs) -> bool:
        """
        Connects to a MySQL database using the provided connection information

        Args:
            `con`: Receives the path to the JSON file or a dictionary
            `**kwargs`: List of parameters for connection
        Returns:
            `bool`: True if the connection was successful otherwise None
        Raises:
            - ValueError
                - You forgot to pass arguments.
                - Forgot a parameter
                - The key is empty.

            - Exception
                - `BirdSystemError.stack_fun`: Pointer to the above errors
        """
        try:
            if isinstance(con, str):
                arq_ = self.filepath_system(con)
                with open(arq_, 'r') as file_json:
                    con = dict(json.load(file_json))

            if kwargs:
                con.update(kwargs)

            if not bool(con):
                raise ValueError('You forgot to pass arguments')

            con = list(zip(con.keys(), con.values()))
            con = dict(filter(lambda t: t[0] in self.__BASE_CONECT, con))

            keys_dic = list(con.keys())
            qtd_keys = len(keys_dic)
            if qtd_keys <= 2:
                raise ValueError(f'Forgot a parameter {keys_dic}')

            for k in keys_dic:
                if con[k] is None:
                    raise ValueError(f'The "{k}" key is empty')

            if 4 == qtd_keys and ('data_base' in keys_dic):
                self.__conn = mysql.connector.connect(
                    host=con['host'],
                    user=con['user'],
                    password=con['pass_'],
                    database=con['data_base']
                )
            elif 3 == qtd_keys and ('data_base' not in keys_dic):
                self.__conn = mysql.connector.connect(
                    host=con['host'],
                    user=con['user'],
                    password=con['pass_']
                )

            self.__cursor_ = self.__conn.cursor()
            self.__debug_conn = con
            self.__BASE_CONECT.update(con)
            return True
        except Exception as err:
            print(self.stack_func(self.__CLASS_NAME, err))


    def get_conn(self) -> dict:
        """get connection dictionary"""
        try:
            conex = self.__conn.is_connected()
            dicio_conex = isinstance(self.__debug_conn, dict)

            if conex and dicio_conex:
                return self.__debug_conn
        except Exception as err:
            err = 'You are connected ?' if 'NoneType' in str(err) else str(err)
            print(self.stack_func(self.__CLASS_NAME, err))


    def get_cursor(self) -> CMySQLCursor:
        """get custom MySQL cursor"""
        try:
            if self.__conn.is_connected():
                self.__cursor_ = self.__conn.cursor()
                return self.__cursor_
        except Exception as err:
            err = 'You are connected ?' if 'NoneType' in str(err) else str(err)
            print(self.stack_func(self.__CLASS_NAME, err))


    def descon(self) -> None:
        """Closes the connection to MySQL and the cursor"""
        try:
            if isinstance(self.__cursor_, CMySQLCursor):
                self.__cursor_.close() 
                self.__cursor_ = None

            if isinstance(self.__conn, CMySQLConnection):
                self.__conn.close()
                self.__conn = None
        except Exception as err:
            print(self.stack_func(self.__CLASS_NAME, err))


if __name__ == '__main__':
    bird_mysql = BirdMySQL()
    src = os.path.dirname(__file__)

    json_ = os.path.join(src, 'config', 'ignore_test.json')
    bird_mysql.conn_mysql(json_)
