import logging 
import pymongo_inmemory
from pymongo import MongoClient, errors
# -> TODO: Implement FinMongo.__str__
# TODO: Modify FinMongo to take logger as a optional parameter, if its not given, we just setup a stream handler

class FinMongo:
    """ 
    -----------------------------------------------------------
    Purpose
    -----------------------------------------------------------
    - A class used to represent a MongoDB connection handler.
    
    -----------------------------------------------------------
    Attributes
    -----------------------------------------------------------
    - host (str): a string containing the host connection string for MongoDB
    - logger (Logger): a logger object used for logging connection and disconnection events
    - client (MongoClient): a MongoClient object that maintains the connection to the MongoDB server
    """

    def __init__(self, host: str = None):
        """
        -----------------------------------------------------------
        Purpose
        -----------------------------------------------------------
        - Constructs a new 'FinMongo' object and establishes a connection to the MongoDB server.
        
        -----------------------------------------------------------
        Parameters
        -----------------------------------------------------------
        - host (str): The host connection string for MongoDB.
        
        -----------------------------------------------------------
        Raises
        -----------------------------------------------------------
        - ConnectionFailure: If the connection to the MongoDB server fails.
        """
        
        # Setup logger and level
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Create the stream handler
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)

        # Create the file handler
        file_handler = logging.FileHandler('FinMongo.log')
        file_handler.setLevel(logging.ERROR)

        # Create formatter and add it to the file and stream handler
        formatter = logging.Formatter('%(asctime)s/%(name)s/%(levelname)s:: %(message)s')
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)
        
        if host==None:
            # If no host connection str was given, create and return an in-memory database
            self.client = pymongo_inmemory.MongoClient()
            self.logger.info("Successfully created a in-memory MongoDB.")
        else:
            # Establish connection with mongo cluster
            try:
                self.client = MongoClient(host) # host connection string
                self.client.server_info()  # force connection request for testing 
            except errors.ConnectionFailure:
                self.logger.exception("Could not connect to MongoDB (Error: Connection Failure).")   
            else: 
                self.logger.info("Successfully connected to MongoDB.")
            
        return

    def connect(self):
        """
        -----------------------------------------------------------
        Purpose
        -----------------------------------------------------------
        - A placeholder for handling multiple connections. 
        - This method is not yet implemented.
        """
        return

    def disconnect(self):
        """
        -----------------------------------------------------------
        Purpose
        -----------------------------------------------------------
        - Closes the connection to the MongoDB server.

        -----------------------------------------------------------
        Parameters
        -----------------------------------------------------------
        - None

        -----------------------------------------------------------
        Returns
        -----------------------------------------------------------
        - Success (bool): True if the connection was successfully closed, False otherwise.

        -----------------------------------------------------------
        Raises
        -----------------------------------------------------------
        - Exception: If an exception occurred while closing the connection.
        """
        success = False
        if self.client: 
            try: self.client.close()
            except: self.logger.error("Failed to close the connection.")
            else: 
                self.logger.info("Sucessfully closed the connection.")
                success = True
        return success

    def __str__(self): # Print the status (connection overview) and other information
        """
        -----------------------------------------------------------
        Purpose
        -----------------------------------------------------------
        - Returns a string representation of the MongoDB server's status and other information.
        
        -----------------------------------------------------------
        Parameters
        -----------------------------------------------------------
        - None
        
        -----------------------------------------------------------
        Returns
        -----------------------------------------------------------
        - str: A string with the MongoDB server's information.
        """
        # sample_info_server_not_in_memory = {'version': '6.0.6', 'gitVersion': '26b4851a412cc8b9b4a18cdb6cd0f9f642e06aa7', 'modules': ['enterprise'], 'allocator': 'tcmalloc', 'javascriptEngine': 'mozjs', 'sysInfo': 'deprecated', 'versionArray': [6, 0, 6, 0], 'bits': 64, 'debug': False, 'maxBsonObjectSize': 16777216, 'storageEngines': ['devnull', 'ephemeralForTest', 'inMemory', 'queryable_wt', 'wiredTiger'], 'ok': 1.0, '$clusterTime': {'clusterTime': Timestamp(1686251487, 4), 'signature': {'hash': b'\x0b\xcc*\xc1\x81\xd9\xebv\x06\xcc\xc05\x9e+\t\xfe&\x1d\xab)', 'keyId': 7204913445559336962}}, 'operationTime': Timestamp(1686251487, 4)}
        # TODO: Take the sample info and create a string with the important sections for the user
        # TODO: (Alternative) Can show other information like the databases, collections, collection metrics (num of documents) and so on
        return str(self.client.server_info())


if __name__ == "__main__": 
    import os 
    from dotenv import load_dotenv
    load_dotenv()
    
    MONGO_USER = os.getenv('MONGO_USER')
    MONGO_PASS = os.getenv('MONGO_PASS') 
    handler = FinMongo(f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@cluster0.lvkyalc.mongodb.net/?retryWrites=true&w=majority") #TODO: Add ENV var handling functionality    
    #handler = FinMongo() # in-memory
    client = handler.client

    # Code to test db, collection, and document creation
    # In MongoDB, db's and collections are not created untill they have data added to them
    mydb = client["mydatabase"]
    mycol = mydb["users"]
    sample_data = {
        "date_created": None,
        "user_id": 0, "username": "Harri",
        # For analytical purposes
        "major":"CS", "year": 3,
        "email": None, "password": None
    }

    x = mycol.insert_one(sample_data)

    print(client.list_database_names())
    print(mydb.list_collection_names())
    print(x.inserted_id)
    
    handler.disconnect() # Disconnect the handler (and the MongoDB client) after use