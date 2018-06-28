import unittest
import time, os



class MyTests(unittest.TestCase):

    def test1(self):
        # test code here
        pass

    def test2(self):
        # test code here
        pass

class MyOtherTests(unittest.TestCase):
    def test1(self):
        # test code here
        pass

    def test2(self):
        # test code here
        pass

suite1 = unittest.TestLoader().loadTestsFromTestCase(MyTests)
suite2 = unittest.TestLoader().loadTestsFromTestCase(MyOtherTests)

all_tests = unittest.TestSuite([suite1,suite2])

unittest.TextTestRunner().run(all_tests)

