# python 3.12.3
import os
import sys
import pytest
from pathlib import Path
from src.bird import BirdSystemError, BirdSystem

src = os.path.dirname(Path(__file__).parent)
src = os.path.join(src, 'src')
sys.path.append(src)


@pytest.fixture
def excep():
    return BirdSystemError()


def test_raise_pers_and_atribut(excep):
    assert excep.msg is None
    excep.msg = 'Test msg error'
    assert isinstance(excep.msg, str)
    excep.raise_pers(error='Not is error')
    assert excep.msg is 'Not is error'


def test_stack_function(excep):
    class_name = 'testclass'
    error = ValueError('My error')
    result = excep.stack_func(class_=class_name, error=error)
    assert isinstance(result, str)
    assert class_name in result
    assert str(error) in result


@pytest.fixture
def bird_system():
    return BirdSystem()


def test_filepath_system_existing_file(bird_system, tmp_path):
    file_path = tmp_path / "teste_file.txt"
    file_path.touch()
    result = bird_system.filepath_system(file_path)
    assert isinstance(result, str)
    assert str(file_path.resolve()) in result


def test_filepath_system_non_existing_file(bird_system):
    non_existing_file = "non_existing_file.txt"
    exce = bird_system.filepath_system(non_existing_file)
    assert f'File "{non_existing_file}" not found' in exce


def test_filepath_system_windows_path(bird_system, tmp_path, monkeypatch):
    monkeypatch.setattr("platform.system", lambda: "Windows")
    file_path = tmp_path / "teste_file.txt"
    file_path.touch()
    result = bird_system.filepath_system(file_path)
    assert isinstance(result, str)
    assert "\\" in result
