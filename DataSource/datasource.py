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

    def getDataInRange(self, dataset, fromDate, toDate= "2019-10-09"):
        '''
        Returns a list containing data within given range for specified dataset

        Returns: a list of all data within range.
        '''
        try:
            cursor = connection.cursor()
            query = "SELECT	* FROM {0} WHERE (pricedate BETWEEN '{1}' AND '{2}')".format(dataset, fromDate, toDate)
            cursor.execute(query)
            return cursor.fetchall()

        except Exception as e:
            print("Something went wrong when executing the query: ", e)
            return None

    def getDataOfType(self, dataset, datatype):
        pass

    def performAnalysisQuery(self, datasets, datatype, analysistype, toDate):
        pass
    
    def performDataQuery(self, datasets, datatype, fromDate, toDate):
        returnData = []
        for dataset in datasets:
            tempData = getDataInRange(dataset, fromDate, toDate)
            tempData = getDataOfType(tempData, datatype)
            returnData.append(tempData)
        return returnData

