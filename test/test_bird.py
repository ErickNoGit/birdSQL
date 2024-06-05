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


def test_stack_function(excep):
    class_name = 'testclass'
    error = ValueError('My error')
    result = excep.stack_func(class_name, error)
    assert isinstance(result, str)
    assert class_name in result
    assert str(error) in result


def test_manager_error_local_stack(excep):
    class_name = 'fake_class'
    raise_fake = ValueError('My exception')
    assert excep.show_stack_err() == [None]
    assert excep.manager_error(class_name, raise_fake) is None
    assert bool(excep.show_stack_err()) is True
    assert len(excep.show_stack_err()) > 1


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
