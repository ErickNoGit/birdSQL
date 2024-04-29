import inspect
import platform
from os import PathLike, path
from typing import Union


class ExceptMethod:
    """Customized error log for each method"""
    
    def stack_func(self, error: Union[Exception, ValueError], class_: str) -> str:
        """Use an error to return a function"""
        frame_ = inspect.stack()[1]
        return f'Error method -> "{class_ + '.' + frame_.function}": {error}'


class BirdSystem(ExceptMethod):
    """Controls data types for operating systems"""

    def __init__(self) -> None:
        super().__init__()


    def filepath_siystem(self, file: Union[str, PathLike]) -> str:
        """returns the absolute path of a file according to the operating system"""
        try:
            if not path.exists(file):
                raise ValueError(f'File "{file}" not found')

            plat_ = platform.system()

            if plat_ == 'Windows':
                return str(path.abspath(file)).replace("/", "\\")
        except Exception as err:
            class_name = str(self.__class__.__name__)
            return self.stack_func(error=err, class_=class_name)


if __name__ == '__main__':
    bs = BirdSystem()
    arq_ = './src/config/basic_conecfeast.json'
    path_like = bs.filepath_siystem(file=arq_)
    print(path_like)