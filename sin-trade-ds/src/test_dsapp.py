import pytest
# `from dsapp import main` is importing the `main` function from the `dsapp` module. This allows you
# to use the `main` function in your test script without having to prefix it with the module name
# every time you call it.
from dsapp import main

def test_main():
    string = main()
    assert "you have made a successful call" in string
 