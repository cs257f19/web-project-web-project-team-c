from datasource import *
import unittest
import datetime


class DataSourceTester(unittest.TestCase):
    def test_dateToIntCoversion(self):
        ds = DataSource("User", "Password")
        x = datetime.datetime(2020, 5, 17)
        self.assertEqual(20200517, ds.dateTimeToInt(x))
    def test_not_datetime_dateToIntConversion(self):
        ds = DataSource("User", "Password")
        x = "hello"
        self.assertEqual(0, ds.dateTimeToInt(x))

if __name__ == '__main__':
    unittest.main()
