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

    def getDataOfType(self, dataset, datatype):
        '''
        Returns a collection containing the pricedate and the selected datatype for a given dataset
        dataset: list of lists containing data from the database
        datatype: string name of datatype
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

    def performDataQuery(self, datasets, datatype, fromDate, toDate):
        returnData = []
        for setname in datasets:
            tempData = getData(setname)
            tempData = getDataInRange(tempData, fromDate, toDate)
            tempData = getDataOfType(tempData, datatype)
            returnData.append(tempData)
        return returnData

    def getTrendline(self, dataset, trendtype):
        pass

    def graphData(self, dataset, trendline, color, style):
        pass