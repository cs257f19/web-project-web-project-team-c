import psycopg2
import getpass
import datetime
import numpy as np
# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split

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
            connection = psycopg2.connect(database=self.user, user=self.user, password=self.password)
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
            query = "SELECT pricedate, {0} FROM {1} WHERE pricedate BETWEEN to_date({2}::text, 'YYYYMMDD') AND to_date({3}::text, 'YYYYMMDD')".format(dataType, setname, fromDate, toDate)
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print("Error while executing query: ", e)
            return []

    def dateTimeToInt(self, dt_time):
        '''
        Converts dt_time to an int.
        dt_time: Datetime format
        
        Returns: date in integer format YYYYMMDD
        '''
        if (type(dt_time) != datetime.date):
            return 0

        return 10000*dt_time.year + 100*dt_time.month + dt_time.day

#     def performAnalysisQuery(self, regressandDatasets, regressorDatasets, regressand, regressor, regressionType, fromDate, toDate=20191009):
#         '''
#         Executes all the necessary functions in order to perform analysis on a set (or sets) of data and returns a list of lists containing that data
#         regressandDatasets: string name of the regressandDataset
#         regressorDatasets: string name of the regressorDataset
#         regressand: string name of regressand
#         regressor: string name of regressor
#         regressionType: string name of regression type
#         '''
#         regressandData = self.performDataQuery([regressandDatasets], regressand, fromDate, toDate=20191009)
#         regressorData = self.performDataQuery([regressorDatasets], regressor, fromDate, toDate=20191009)
#         return doRegressionAnalysis(regressandData, regressorData, regressionType)
# 
#     def doRegressionAnalysis(self, regressand, regressor, regressionType):
#         '''
#         Returns a list containing a string of whether to buy stock or not and the probability that the stock will increase in price.
#         regressand: the target value (most likely the stock price or a boolean of either positive or negative change - stock price change)
#         regressor: list of variables that are going to be used to impact target value
#         regressionType: type of regression analysis to perform (linear, lasso, polynomial of degree n)
#         '''
#         if regressionType == "linear":
#         	return self.linearRegression(regressand, regressor)
#         return -1
#         
#             
#     def linearRegression(self, regressand, regressor):
#     	'''
#     	regressand: the target value (most likely the stock price or a boolean of either positive or negative change - stock price change)
#     	regressor: list of variables that are going to be used to impact target value
#     	'''
#     	
#     	x_value_data = regressor
#     	y_value_data = regressand
#     	X_train, X_test, y_train, y_test = train_test_split(x_value_data, y_value_data, test_size=0.33, random_state=42)
#     	regr = linear_model.LinearRegression()
#     	regr.fit(X_train, y_train)
#     	y_pred = regr.predict(X_test)
#     	if regr.coef_ > 0:
#     		return [True, y_pred, X_test]
#     	else:
#     		return [False, y_pred, X_test]
