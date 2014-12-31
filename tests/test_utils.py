#!/usr/bin/env python
# -*- coding: utf-8 -*-

from topogram.utils import any2utf8, any2unicode
import unittest

class TestUtils(unittest.TestCase):

        def test_any2utf8(self):
            s = "你好".decode('utf-8')
            uni = any2unicode(s)
            self.assertTrue(isinstance(uni, unicode))

        def test_any2utf8(self):
            s = any2utf8("你好")
            self.assertTrue(isinstance(s, str))

if __name__ == '__main__':
    unittest.main()
