from datasource import *
import unittest
import datetime


class DataSourceTester(unittest.TestCase):
    def setUp(self):
        self.ds = DataSource("hayesrichn","orange227blue")
        self.datasetRange = self.ds.getData("btc")
        self.datasetType = self.ds.getDataInRange(datasetRange, 20100717, 20100718)
    def test_date_to_int(self):
        result = datetime.date(2020, 5, 17)
        self.assertEqual(20200517, self.ds.dateTimeToInt(result))
    def test_not_datetime_date_to_int(self):
        result = "hello"
        self.assertEqual(0, self.ds.dateTimeToInt(result))
    def test_get_data(self):
        result = (datetime.date(2010, 7, 17), 0.04951, 0.04951, 0.04951, 0.04951, 0.04951, 0)
        self.assertEqual(result, self.ds.getData("btc")[0])
    def test_get_data_in_range(self):
        result = [(datetime.date(2010, 7, 17), 0.04951, 0.04951, 0.04951, 0.04951, 0.04951, 0), (datetime.date(2010, 7, 18), 0.04951, 0.08585, 0.05941, 0.08584, 0.08584, 5)]
        self.assertEqual(result, self.ds.getDataInRange(datasetRange, 20100717, 20100718))
    def test_get_data_of_type(self):
        result = [(datetime.date(2010, 7, 17), 0.04951), (datetime.date(2010, 7, 18), 0.04951)]
        self.assertEqual(result, self.ds.getDataOfType(self.datasetType, "openprice"))
    def test_perform_data_query(self):
        result = [[(datetime.date(2010, 7, 17), 0.04951), (datetime.date(2010, 7, 18), 0.04951)], [(datetime.date(2010, 7, 17), 0.04951), (datetime.date(2010, 7, 18), 0.04951)]]
        self.assertEqual(result, self.ds.performDataQuery(["btc", "btc"], "openprice", 20100717, 20100718))


if __name__ == '__main__':
    unittest.main()