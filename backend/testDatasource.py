from datasource import *
import unittest
import datetime


class DataSourceTester(unittest.TestCase):
    def test_dateToTimeCoversion(self):
        ds = DataSource("User", "Password")
        x = datetime.datetime(2020, 5, 17)
        self.assertEqual(20200517, datasource.)


if __name__ == '__main__':
    unittest.main()
