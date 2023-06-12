from FinMongo import FinMongo
from datetime import datetime as dt
#TODO: Add logger (take logger as a optional parameter too)
#TODO: Add functionality to insert many in user create
#TODO: Support multi field query (e.x., user_id : x or y) (<- this is just changing the query dictionary that is passed)
#TODO: Finish delete and update
#TODO: Writing testing code in main

class User:
    def __init__(self, collection=None): 

        # General Attributes:
        if collection==None: # When no collection is given, create a mongoDB and the required 'users' collection
            self.mongo = FinMongo()
            self.database = self.mongo.client['db']
            self.collection = self.database['users']
        else: self.collection = collection

        # User Specific Attributes/Properties:
        self._id = None # This is get/set using getter/setter methods
        return

    @property 
    def id(self): # NOTE: ID Getter
        return self._id
    
    @id.setter
    def id(self, value:int): # NOTE: ID Setter (to switch ID's and run queries?)
        if value<0: raise Exception("Invalid ID. ID should be > 0")
        self._id = value
        return

    def _validate(self, data: dict) -> bool: # Internal function used for validating a data dictionary 
        valid = True
        if data['user_id']<0: 
            valid = not valid
            raise Exception("Invalid User ID, must be zero or positive.")
        if data['username']==None or data['username']=="": 
            valid = not valid
            raise Exception("Username cannot be empty or none.")
        return valid

    # User(s) CRUD functions
    def create(self, data=None): # This functoin creates a user document and then returns the document ID(s) to the user 
        
        if data==None: # If no data was given, use input statements to get the required information from the user
            
            # Get inputs from user
            user_id = int(input("User ID: "))
            if user_id<0: raise Exception("Invalid User ID, must be zero or positive.")
            username = input("Username: ")
            if username=="" or username==None: raise Exception("Usename cannot be empty or none.")
            major = input("Major: ")
            year = int(input("Year: "))
            
            # Pack inputs into a dictionary (i.e., document to add to the collection)
            data = {
                "date_created": dt.now(),
                "user_id": user_id, "username": username,
                "major":major, "year": year,
            }

        else: 
            # For validating multiple documents (given in a list)
            if isinstance(data, list): 
                for user_data in data:
                    print(user_data)
                    try: self._validate(user_data) # Validates data and raises exceptions     
                    except Exception as e: print(e)
                    else: pass 
            # For validating one document (given as a dict)
            else: self._validate(data) 
            
        return self.collection.insert_one(data).inserted_id
    
    def read(self, query:dict={}) -> list: # Get all the records for this ID, return the JSON's (optionally print and return Pandas DF)
        # Compose a query to read the current user's info if self._id is set and no query was given
        if len(query)==0 and self._id!=None: query = {"user_id": self._id}
        result = list(self.collection.find(query))
        return result

    def delete(self):
        # Given a ID, or a set of IDs, or a JSON with the approprite data, remove the user from the system
        # Perform any calculations, error handling, raise exceptions as required, 
        return
    
    def update(self):
        # Update user profile(s) given JSON information
        return
    

if __name__=='__main__':
    import os 
    from dotenv import load_dotenv
    # Load ENV Variables
    load_dotenv()
    MONGO_USER = os.getenv('MONGO_USER')
    MONGO_PASS = os.getenv('MONGO_PASS') 
    # Setup MongoDB Handler
    db_handler = FinMongo(f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@cluster0.lvkyalc.mongodb.net/?retryWrites=true&w=majority") #TODO: Add ENV var handling functionality    
    #db_handler = FinMongo() # in-memory
    # Connect to DB and Collection
    client = db_handler.client
    database = client["mydatabase"]
    collection = database["users"]
    # Initialize an instance of User with the appropriate collection
    user_handler = User(collection) 
    # Initialize the required sample data
    sample_data = {
        "date_created": dt.now(),
        "user_id": 0, "username": "Harri",
        # For analytical purposes
        "major":"CS", "year": 3,
        "email": None, "password": None
    }
    # Add sample_data to user (can also handle creating multiple users)
    #user_handler.create(sample_data)
    # Disconnect the MongoDB handler
    result = user_handler.read()
    print(result)
    #user_handler.mongo.disconnect() # For in-memory
    db_handler.disconnect()