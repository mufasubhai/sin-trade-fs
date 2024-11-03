import pytest
from app import main

def test_main():
    string = main()
    assert "this has been a success" in string