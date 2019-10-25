import psycopg2
import getpass

class DataSource:
	'''
	DataSource executes all of the queries on the database.
	It also formats the data to send back to the frontend, typically in a list
	or some other collection or object.
	'''

    def __init__(self):
        pass

    def connect(user, password):
        '''
        Establishes a connection to the database with the following credentials:
            user - username, which is also the name of the database
            password - the password for this database on perlman

        Returns: a database connection.

        Note: exits if a connection cannot be established.
        '''
        try:
            connection = psycopg2.connect(database=user, user=user, password=password)
        except Exception as e:
            print("Connection error: ", e)
            exit()
        return connection

    def getDataInRange(self, start, end=10.0):
        '''
        Returns a list of all of the magnitudes from the specified starting magnitude until the specified ending magnitude.

        PARAMETERS:
            start - the low end of the magnitude range
            end - the high end of the magnitude range (default: 10.0)

        RETURN:
            a list of all of the earthquake events with magnitudes in the specified range
        '''
        return []

    def getQuakesOnContinent(self, continent):
        '''
        Returns a list of all of the earthquakes that occurred on the specified continent.

        PARAMETERS:
            continent 
        
        RETURN:
            a list of all of the earthquake events that occurred on this continent
        '''
        return []

    def getQuakesInDateRange(self, start, end):
        '''
        Returns a list of all of the earthquakes that occurred within the range of specified dates.

        PARAMETERS:
            start - the starting date of the range
            end - the ending date of the range

        RETURN:
            a list of all of the earthquake events that occurred within this date range.
        '''
        return []


    def main():
        # Replace these credentials with your own
        user = 'adalal'
        password = getpass.getpass()

        # Connect to the database
        connection = connect(user, password)

        # Execute a simple query: how many earthquakes above the specified magnitude are there in the data?
        results = getQuakesAboveMagnitude(connection, 5)

        if results is not None:
            print("Query results: ")
            for item in results:
                print(item)

        # Disconnect from database
        connection.close()
