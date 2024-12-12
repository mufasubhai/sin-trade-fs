import pytest
from app_be import main

def test_main():
    string = main()
    assert "this has been a success" in string