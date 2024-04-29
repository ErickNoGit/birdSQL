import json
import mysql.connector
from os import path, PathLike
from typing import Tuple, Union

from bird import BirdSystem


class BirdMySQL(BirdSystem):
    """Responsible for all functions linked to MySQL"""

    def __init__(self) -> None:
        """Loads basic connection data"""
        super().__init__()

        self.base_conect = {
            'host': None,
            'user': None,
            'pass': None,
            'data_base': None
        }


    def read_json_conect(self, file: Union[str, PathLike]) -> dict:
        """Read connection json file"""
        try:
            arq_ = self.filepath_siystem(file)

            if 'Error method' in arq_:
                raise ValueError(f'File "{file}" not found')

            with open(arq_, 'r') as file_json:
                return dict(json.load(file_json))
        except Exception as err:
            class_name = str(self.__class__.__name__)
            print(self.stack_func(error=err, class_=class_name))


if __name__ == '__main__':
    bird_mysql = BirdMySQL()
    src = path.dirname(__file__)

    json_ = path.join(src, 'config', 'basic_conect.json')
    dicio_ = bird_mysql.read_json_conect(json_)
    print(dicio_)
