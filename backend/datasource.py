import psycopg2
import getpass

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
            exit()
        return connection

    def closeConnection(self):
        self.connection.close()

    def getDataInRange(self, dataset, fromDate, toDate=20191009):
        '''
        Returns a collection containing data within given range for specified dataset
        dataset: list of lists containing data from the database
        fromDate and toDate: date in integer format YYYYMMDD

        Returns: a collection of all data within range.
        '''
        returnData = []
        if dataset != []:
            for dataRow in dataset:
                if fromDate <= dataRow[0] <= toDate:
                    returnData.append(dataRow) 

        return returnData

    def getDataOfType(self, dataset, dataType):
        '''
        Returns a collection containing the pricedate and the selected datatype for a given dataset
        dataset: list of lists containing data from the database
        dataType: string name of data type
        '''
        pass

    def getData(self, setname):
        try:
            cursor = connection.cursor()
            query = "SELECT	* FROM {0}".format(setname)
            cursor.execute(query)
            return cursor.fetchall()

        except Exception as e:
            print("Something went wrong when executing the query: ", e)
            return []

    def performDataQuery(self, datasets, dataType, fromDate, toDate):
        '''
        Executes all the necessary functions to return a list of lists containing data of a certain type in a given range
        datasets: list of string names of datasets
        dataType: string name of data type
        fromDate and toDate: date in integer format YYYYMMDD
        '''
        returnData = []
        for setname in datasets:
            tempData = getData(setname)
            tempData = getDataInRange(tempData, fromDate, toDate)
            tempData = getDataOfType(tempData, dataType)
            returnData.append(tempData)
        return returnData

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
        pass

    def doLassoRegression(self, dataset):
        pass

    def doBackProp(self, dataset):
        pass

    def graphData(self, dataset, color, style, trendline=None):
        pass