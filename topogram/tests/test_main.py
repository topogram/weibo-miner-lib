from unittest import TestCase

import topogram

class TestTopogram(TestCase):
    def test_is_string(self):
        s = topogram.check()
        self.assertTrue(isinstance(s, basestring))
