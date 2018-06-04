import unittest
import mock
from lab1 import proceed

class proceedTest(unittest.TestCase):
    list1 = ["https://rutracker.org/forum/viewforum.php?f=5", "https://pastebin.com"]
    @mock.patch('lab1.proceed', side_effect=[2,2,0])
    def testNumberOfEmails(self, proceed):
        self.assertEqual(proceed(self.list1, 1), 2)
        self.assertEqual(proceed(self.list1[0:1], 1), 2)
        self.assertEqual(proceed(self.list1[1:], 1), 0)

if __name__ == '__main__':
    unittest.main()
        