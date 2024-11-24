import pytest
from Source.Database.database import Database

@pytest.mark.parametrize("user, password, expected", [
    ("root", "!Cd2@5Cprb", None),
    ("root", "", 1045),
    ("", "!Cd2@5Cprb", 1045),
    ("", "", 1045)
])
def test_Database_connect(user:str, password:str, expected):
    database = Database()
    assert database.connect(user=user, password=password) == expected