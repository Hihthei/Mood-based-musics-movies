import pytest
from mysql.connector.cursor_cext import CMySQLCursor
from Source.sql.sql import sql_show_databases


@pytest.mark.parametrize("password, expected", [
    ("!Cd2@5Cprb", CMySQLCursor),
    ("", type(None))
])
def test_sql_show_databases(password:str, expected):
    assert type(sql_show_databases(password)) == expected