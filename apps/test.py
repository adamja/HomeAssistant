class Test():
    def __init__(self):
        self.test = "Test return"
        
    def log(self):
        return self.test
        
        
"""
Using this function:

from test import Test

        self.test = Test()
        self.log(self.test.log())
"""