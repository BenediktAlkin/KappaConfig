import unittest
from kappaconfig.entities.wrappers import KCDict

class TestWrappers(unittest.TestCase):
    def test_nonstring_keys(self):
        self.assertEqual(6, KCDict({5: 6})[5])
        self.assertEqual(3, KCDict({False: 3})[False])
        self.assertEqual("float", KCDict({3.2: "float"})[3.2])