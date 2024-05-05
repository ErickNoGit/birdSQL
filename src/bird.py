# Python 3.12.3
import os
import sys
import inspect
import platform
from os import PathLike
from pathlib import Path
from typing import Union

src = os.path.dirname(Path(__file__))
sys.path.append(src)


class BirdSystemError:
    """Customized error log for each method"""
    def __init__(self) -> None:
        self.msg = None


    def raise_pers(self, error: str):
        """Customize error message attribute"""
        self.msg = error


    def stack_func(self, class_: str, error: str) -> str:
        """Use an error to return a function"""
        if self.msg:
            error = self.msg

        func = inspect.stack()[1].function
        err = f'"{class_ + '.' + func}": {error}'
        return f'Error method -> {err}'


class BirdSystem(BirdSystemError):
    """Controls data types for operating systems"""
    def __init__(self) -> None:
        super().__init__()


    def filepath_system(self, file: Union[str, PathLike]) -> str:
        """
        returns the absolute path of a file according to the operating system

        Args:
            `file`: File path
        Returns:
            `str`: Absolute file path
        Raises:
            - ValueError
                - File path not found.

            - Exception
                - `BirdSystemError.stack_fun`: Pointer to the above error
        """
        try:
            if not os.path.exists(file):
                raise ValueError(f'File "{file}" not found')

            if platform.system() == 'Windows':
                return str(os.path.abspath(file)).replace("/", "\\")
        except Exception as err:
            self.raise_pers(err)
            class_name = str(self.__class__.__name__)
            return self.stack_func(class_name, self.msg)


if __name__ == '__main__':
    bs = BirdSystem()
    arq_ = './src/config/basic_conect.json'
    path_like = bs.filepath_system(file=arq_)
    print(path_like)