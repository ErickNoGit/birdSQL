# Python 3.12.3
import os
import sys
import pytest
from pathlib import Path
from mysql.connector.cursor_cext import CMySQLCursor

src = os.path.dirname(Path(__file__).parent)
src = os.path.join(src, 'src')
sys.path.append(src)

from src.bird import BirdSystem
from src.bird_mysql import BirdMySQL


@pytest.fixture
def bird():
    return BirdSystem()


@pytest.fixture
def bird_mysql():
    return BirdMySQL()


def test_conn_mysql_false_arquivo(bird_mysql, bird):
    false_arq = 'test_false.json'
    bird_mysql.conn_mysql(false_arq)
    assert None == bird.msg
    result = bird_mysql.conn_mysql(false_arq)
    assert result == None


def test_conn_mysql_true_arq(bird_mysql):
    json_ = os.path.join(src, 'config', 'ignore_test.json')
    assert bird_mysql.msg is not json_
    assert isinstance(bird_mysql.conn_mysql(json_), bool)
    assert bird_mysql.descon() == None


def test_conn_mysql_error_parameter(bird_mysql):
    assert bird_mysql.conn_mysql() is None
    dicio = {
        'logica': 'error',
        'host': None
    }
    assert bird_mysql.conn_mysql(dicio) is None
    dicio = {
        'host': None,
        'user': None,
        'pass_': None,
        'data_base': None
    }
    assert bird_mysql.conn_mysql(dicio) is None


def test_conn_mysql_conex(bird_mysql):
    json_ = os.path.join(src, 'config', 'ignore_test.json')
    assert bird_mysql.conn_mysql(json_) is True
    assert bird_mysql.conn_mysql(json_) is not None


def test_get_conn_desconect(bird_mysql):
    assert bird_mysql.get_conn() is None
    json_ = os.path.join(src, 'config', 'ignore_test.json')
    bird_mysql.conn_mysql(json_)
    assert isinstance(bird_mysql.get_conn(), dict)
    assert bird_mysql.get_conn() is not None
    bird_mysql.descon()


def test_get_cursor_deconect(bird_mysql):
    assert bird_mysql.get_cursor() is None
    json_ = os.path.join(src, 'config', 'ignore_test.json')
    bird_mysql.conn_mysql(json_)
    assert isinstance(bird_mysql.get_cursor(), CMySQLCursor)
    assert bird_mysql.get_cursor() is not None
    bird_mysql.descon()


def test_desconn_types(bird_mysql):
    assert bird_mysql.get_conn() is None
    assert bird_mysql.get_cursor() is None
    json_ = os.path.join(src, 'config', 'ignore_test.json')    
    bird_mysql.conn_mysql(json_)
    assert isinstance(bird_mysql.get_conn(), dict)
    assert isinstance(bird_mysql.get_cursor(), CMySQLCursor)
    bird_mysql.descon()
    assert bird_mysql.get_conn() is None
    assert bird_mysql.get_cursor() is None
