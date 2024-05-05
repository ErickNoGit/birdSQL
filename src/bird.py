import inspect
import platform
from os import PathLike, path
from typing import Union


class ExceptMethod:
    """Customized error log for each method"""
    def __init__(self) -> None:
        pass
    
    def stack_func(self, class_: str, error: Exception) -> str:
        """Use an error to return a function"""
        err = f'"{class_ + '.' + inspect.stack()[1].function}": {error}'
        return f'Error method -> {err}'


class BirdSystem(ExceptMethod):
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
                - `ExceptMethod.stack_fun`: Pointer to the above error
        """
        try:
            if not path.exists(file):
                raise ValueError(f'File "{file}" not found')

            if platform.system() == 'Windows':
                return str(path.abspath(file)).replace("/", "\\")
        except Exception as err:
            class_name = str(self.__class__.__name__)
            return self.stack_func(error=err, class_=class_name)


if __name__ == '__main__':
    bs = BirdSystem()
    arq_ = './src/config/basic_conecfeast.json'
    path_like = bs.filepath_system(file=arq_)
    print(path_like)