import psycopg2
import getpass
import datetime

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
            return 1
        return connection

    def closeConnection(self):
        self.connection.close()
        
    def performDataQuery(self, datasets, dataType, fromDate, toDate):
        '''
        Executes all the necessary functions to return a list of lists containing data of a certain type in a given range
        datasets: list of string names of datasets
        dataType: string name of data type
        fromDate and toDate: date in integer format YYYYMMDD
        
        Returns: a list of list of lists of data from the specified tables, 
        		 unless a query fails in which case it returns an empty list and stops the function call
        '''
        if (type(datasets) != [] or type(datasets[0]) != str or type(dataType) != str or type(fromDate) != int or type(toDate) != int):
            return []

        returnData = []
        for setname in datasets:
            tempData = self.getData(setname)
            if tempData != []:
                tempData = self.getDataInRange(tempData, fromDate, toDate)
                tempData = self.getDataOfType(tempData, dataType)
                returnData.append(tempData)
            else:
                return []
        return returnData

    def getData(self, setname):
        '''
    	Returns all data from the specified table in the database
    	setname: string name of the database
    	
    	Returns: a list of lists of data from the specified table
    	'''
        try:
            cursor = self.connection.cursor()
            query = "SELECT	* FROM {0}".format(setname)
            cursor.execute(query)
            return cursor.fetchall()

        except Exception as e:
            print("Something went wrong when executing the query: ", e)
            return []

    def getDataInRange(self, dataset, fromDate, toDate=20191009):
        '''
        Returns a collection containing data within given range for specified dataset
        dataset: list of lists containing data from the database
        fromDate and toDate: date in integer format YYYYMMDD

        Returns: a list of lists of data within the specified range
        '''

        returnData = [] #Why wasn't this here?
        for dataRow in dataset:
            priceDate = self.dateTimeToInt(dataRow[0])
            if fromDate <= priceDate <= toDate:
                returnData.append(dataRow)

        return returnData
        
    def getDataOfType(self, dataset, dataType):
        '''
        Returns a collection containing the pricedate and the selected datatype for a given dataset
        dataset: list of lists containing data from the database
        dataType: string name of data type
        
        Returns: a list of lists of data of the specified type
        '''

        pass

    def dateTimeToInt(self, dt_time):
        '''
        Converts dt_time to an int.
        dt_time: Datetime format
        
        Returns: date in integer format YYYYMMDD
        '''
        if (type(dt_time) != datetime.date):
            return 0

        return 10000*dt_time.year + 100*dt_time.month + dt_time.day

    def performAnalysisQuery(self, datasets, dataType, analysisType):
        '''
        Executes all the necessary functions in order to perform analysis on a set (or sets) of data and returns a list of lists containing that data
        datasets: list of string names of datasets
        dataType: string name of data type
        analysisType: string name of analysis type
        '''
        pass

    def getTrendline(self, dataset, trendType):
        '''
        Returns a string of the best trendline for a given set of data
        dataset: list containing data
        trendType: string name of trend type (linear, exponential, polynomial of degree n, etc.)
        '''
        pass

    def doRegressionAnalysis(self, regressand, regressor, regressionType):
        '''
        Returns a list containing a string of whether to buy stock or not and the probability that the stock will increase in price.
        regressand: the target value (most likely the stock price or a boolean of either positive or negative change - stock price change)
        regressor: list of variables that are going to be used to impact target value
        regressionType: type of regression analysis to perform (linear, lasso, polynomial of degree n)
        '''
        pass

    def graphData(self, dataset, style, colorblindPalette=None, trendline=None):
        '''
    	Return an image of graph based on the specified parameters.
    	dataset: list of lists containing data to be graphed
    	colorblindPalette: string name of colorblindness to correct for
    	style: string name of graph style (bar, line, point)
    	trendline: string of trendline    	
    	'''
        pass
