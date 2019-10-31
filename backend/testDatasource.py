from datasource import *
import unittest
import datetime


class DataSourceTester(unittest.TestCase):
    def setUp(self):
        self.ds = DataSource("hayesrichn","orange227blue")
    def test_dateToIntCoversion(self):
        x = datetime.datetime(2020, 5, 17)
        self.assertEqual(20200517, self.ds.dateTimeToInt(x))
    def test_not_datetime_dateToIntConversion(self):
        x = "hello"
        self.assertEqual(0, self.ds.dateTimeToInt(x))

if __name__ == '__main__':
    unittest.main()
