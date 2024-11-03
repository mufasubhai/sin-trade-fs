import pytest
from beapp import main

def test_main():
    string = main()
    assert "this has been a success" in string