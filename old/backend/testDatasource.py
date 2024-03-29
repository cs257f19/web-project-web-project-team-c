from datasource import *
import unittest
import datetime


class DataSourceTester(unittest.TestCase):
    def setUp(self):
        self.ds = DataSource("hayesrichn","orange227blue")
        self.dataset = self.ds.getData("btc", "openprice", 20100717, 20100718)

    def test_date_to_int(self):
        result = datetime.date(2020, 5, 17)
        self.assertEqual(20200517, self.ds.dateTimeToInt(result))

    def test_not_datetime_date_to_int(self):
        result = "hello"
        self.assertEqual(0, self.ds.dateTimeToInt(result))

    def test_get_data(self):
        result = (datetime.date(2010, 7, 17), 0.04951)
        self.assertEqual(result, self.ds.getData("btc", "openprice", 20100717, 20100718)[0])

    def test_perform_data_query(self):
        result = [[(datetime.date(2010, 7, 17), 0.04951), (datetime.date(2010, 7, 18), 0.04951)], [(datetime.date(2010, 7, 17), 0.04951), (datetime.date(2010, 7, 18), 0.04951)]]
        self.assertEqual(result, self.ds.performDataQuery(["btc", "btc"], "openprice", 20100717, 20100718))

    def test_wrong_dataset_perform_data_query(self):
        result = []
        self.assertEqual(result, self.ds.performDataQuery(["btc", "lemon"], "openprice", 20100717, 20100718))

    def test_wrong_datatype_perform_data_query(self):
        result = []
        self.assertEqual(result, self.ds.performDataQuery(["btc", "btc"], "lemonprice", 20100717, 20100718))

    def test_wrong_datatype_perform_data_query(self):
        result = []
        self.assertEqual(result, self.ds.performDataQuery(["btc", "btc"], "openprice", "2010-07-17", 20100718))

#     def test_linear_regression(self):
#         pass
    


if __name__ == '__main__':
    unittest.main()
