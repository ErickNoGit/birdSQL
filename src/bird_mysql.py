import json
import mysql.connector
from os import path, PathLike
from typing import Tuple, Union
from .bird import BirdSystem


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

        self.obj_conect = None
        self.cursor_ = None


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
                - File path not found.
                - You forgot to pass arguments.
                - Forgot a parameter
                - The key is empty.

            - Exception
                - `ExceptMethod.stack_fun`: Pointer to the above errors
        """
        try:
            if isinstance(con, str):
                arq_ = self.filepath_system(con)
                if 'Error method' in arq_:
                    raise ValueError(f'File "{con}" not found')

                with open(arq_, 'r') as file_json:
                    con = dict(json.load(file_json))

            if bool(kwargs):
                con = kwargs

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
                conn = mysql.connector.connect(
                    host=con['host'],
                    user=con['user'],
                    password=con['pass_'],
                    database=con['data_base']
                )
                self.obj_conect = con
                self.cursor_ = conn.cursor()

                self.__BASE_CONECT['host'] = con['host']
                self.__BASE_CONECT['user'] = con['user']
                self.__BASE_CONECT['pass_'] = con['pass_']
                self.__BASE_CONECT['data_base'] = con['data_base']
                return True
            elif 3 == qtd_keys and ('data_base' not in keys_dic):
                conn = mysql.connector.connect(
                    host=con['host'],
                    user=con['user'],
                    password=con['pass_']
                )
                self.obj_conect = con
                self.cursor_ = conn.cursor()

                self.__BASE_CONECT['host'] = con['host']
                self.__BASE_CONECT['user'] = con['user']
                self.__BASE_CONECT['pass_'] = con['pass_']
                return True
        except Exception as err:
            print(self.stack_func(self.__CLASS_NAME, err))


if __name__ == '__main__':
    bird_mysql = BirdMySQL()
    src = path.dirname(__file__)

    json_ = path.join(src, 'config', 'ignore_test.json')
    con = bird_mysql.conn_mysql(json_)
