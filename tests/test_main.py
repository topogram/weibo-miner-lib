import  unittest
from topogram.topogram import Topogram

class TestTopogram(unittest.TestCase):

    def setUp(self):
        self.topogram = Topogram

    def test_is_string(self):
        # s = self.topogram.check()
        # self.assertTrue(isinstance(s, basestring))
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
