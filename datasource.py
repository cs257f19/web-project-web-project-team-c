# This is the most updated version of our backend, accessible by the server in webapp.py

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs, quote_ident
import getpass
import datetime
import numpy as np

class DataSource:
    '''
    DataSource executes all of the queries on the database.
    It also formats the data to send back to the frontend, typically in a list
    or some other collection or object.
    '''

    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.connection = self.connect()
        self.allowedDatatsets = ["btc", "spy", "gld", "irx"]
        self.allowedDataTypes = ["openprice", "highprice", "lowprice", "closeprice", "adjcloseprice", "volume"]

    def connect(self):
        '''
        Establishes a connection to the database with the following credentials:
            user - username, which is also the name of the database
            password - the password for this database on perlman

        Returns: a database connection.

        Note: exits if a connection cannot be established.
        '''
        try:
            connection = psycopg2.connect(host="localhost", database=self.user, user=self.user, password=self.password)
        except Exception as e:
            print("Connection error: ", e)
            exit(1)
        return connection

    def closeConnection(self):
        self.connection.close()

    def performDataQuery(self, datasets, dataType, fromDate, toDate=20191009):
        '''
        Executes all the necessary functions to return a list of lists containing data of a certain type in a given range
        datasets: list of string names of datasets
        dataType: string name of data type
        fromDate and toDate: date in integer format YYYYMMDD

        Returns: a list of list of lists of data from the specified tables,
        		 unless a query fails in which case it returns an empty list and stops the function call
        '''

        # Check if all dataset names are allowed, the datatype is allowed, and that the two dates are in the correct format
        if ([0 for setname in datasets if setname not in self.allowedDatatsets] != [] or (dataType not in self.allowedDataTypes) or type(fromDate) != int or type(toDate) != int):
            return []

        returnData = []
        for setname in datasets:
            returnData.append(self.getData(setname, dataType, fromDate, toDate))
        return returnData

    def formatData(self, data):
        '''
        data: a list of two lists containing the data retrieved from a query (getData) call
        Returns data formatted for flask (a list of tuples containing (pricedate, price1, price2)).
        '''

        if data == [] or data == [[], []] or data == None:
            return []

        # Iterate over all items in each dataset and create a dictionary with the date : price pairing.
        tempData = []
        for datasetIndex in range(len(data)):
            tempdataset = data[datasetIndex]
            tempdataDict = {}
            for item in tempdataset:
                tempdataDict[self.dateTimeToStr(item[0])] = item[1]
            tempData.append(tempdataDict)


        # Iterate over all items in each dictionary and add a "No Data" price value if that date does not appear in the other dataset
        for datasetIndex in range(len(tempData)):
            for key in tempData[datasetIndex].keys():
                for datasetCounter in range(1, len(tempData) + 1):
                    if key not in tempData[(datasetIndex + datasetCounter)%len(tempData)].keys():
                	    tempData[(datasetIndex + datasetCounter)%len(tempData)][key] = "No Data"

        # Iterate over all items in each dictionary and change null values to "No Data"
        for datasetIndex in range(len(tempData)):
            for (key, value) in tempData[datasetIndex].items():
        	    if value == None:
        		    tempData[datasetIndex][key] = "No Data"

        returndata = []

        for key in sorted(tempData[0].keys()):
            tupleList = [key]
            for datasetIndex in range(len(tempData)):
        	    tupleList.append(tempData[datasetIndex][key])
            tupleToAppend = tuple(tupleList)
            returndata.append(tupleToAppend)

        return returndata


    def getData(self, setname, dataType, fromDate, toDate=20191009):
        '''
    	Returns all data from the specified table in the database of the specified type, and between the specified dates
    	setname: string name of the database
        dataType: string name of data type
        fromDate: integer of start date in format YYYYMMDD
        toDate: integer of end date in format YYYYMMDD

    	Returns: a list of lists of data from the specified table
    	'''
        try:
            cursor = self.connection.cursor()
            '''
            For query building it is not all done qwithin the excute function because table names and dataType cannot be placed within double quotes
            in a query otherwise the query will return no results.
            '''
            query = "SELECT pricedate, {0} FROM {1} WHERE pricedate BETWEEN to_date(%s::text, 'YYYYMMDD') AND to_date(%s::text, 'YYYYMMDD')".format(AsIs(quote_ident(dataType, cursor)), AsIs(quote_ident(setname, cursor)))
            cursor.execute(query, (fromDate, toDate, ))
            return cursor.fetchall()
        except Exception as e:
            print("Error while executing query: ", e)
            return []

    def dateTimeToStr(self, dt_time):
        '''

        Converts dt_time to a str.
        dt_time: Datetime format

        Returns: date in string format YYYY-MM-DD
        '''
        if type(dt_time) != datetime.date:
            return ""

        if dt_time.day < 10:
            return "{0}-{1}-0{2}".format(dt_time.year, dt_time.month, dt_time.day)

        return "{0}-{1}-{2}".format(dt_time.year, dt_time.month, dt_time.day)

    def intToStr(self, dt_time):
        '''
        Converts dt_time int to an str.
        dt_time: date in int format YYYYMMDD

        Returns: date in string format "YYYY-MM-DD"
        '''
        if (type(dt_time) != int):
            return ""

        dt_time_str = str(dt_time)

        return "{0}-{1}-{2}".format(dt_time_str[0:4], dt_time_str[4:6], dt_time_str[6:8])


    def strToInt(self, dt_time):
        '''
        Converts dt_time string to an int.
        dt_time: date in string format "YYYY-MM-DD"

        Returns: date in integer format YYYYMMDD
        '''
        if (type(dt_time) != str):
            return 0
        dt_time_list = dt_time.split("-")

        return 10000*int(dt_time_list[0]) + 100*int(dt_time_list[1]) + int(dt_time_list[2])

    def dateTimeToInt(self, dt_time):
        '''

        Converts dt_time to an int.
        dt_time: Datetime format

        Returns: date in integer format YYYYMMDD
        '''
        if (type(dt_time) != datetime.date):
            return 0

        return 10000*dt_time.year + 100*dt_time.month + dt_time.day
