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
        self.__stack_msg_err = [None]


    def show_stack_err(self) -> list:
        """Show error log"""
        print(self.__stack_msg_err)
        return self.__stack_msg_err    


    def stack_func(self, name_class: str, error: Exception) -> str:
        """Use an error to return a function"""
        func = inspect.stack()[2].function
        err = f'"{name_class + '.' + func}": {error}'
        return f'Error method -> {err}'


    def manager_error(self, class_: str, err: Exception) -> None:
        """Manages the insertion of errors into the stack"""
        err = self.stack_func(class_, err)
        if self.__stack_msg_err[-1] != err:
            self.__stack_msg_err.append(err)


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
            class_name = str(self.__class__.__name__)
            self.manager_error(class_name, err)
            return self.stack_func(class_name, err)


if __name__ == '__main__':
    bs = BirdSystem()
    arq_ = './src/config/basic_conect.json'
    path_like = bs.filepath_system(file=arq_)
    print(path_like)