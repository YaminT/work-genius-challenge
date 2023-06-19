import os

def pytest_configure(config):
    import sys
    sys._called_from_test = True

try:
    os.remove("test.db")
except:
    pass