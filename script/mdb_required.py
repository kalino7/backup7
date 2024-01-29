"""required module fxns or objects used among multiple files"""
import os
import requests
from dotenv import load_dotenv
from pymongo import MongoClient

# DB connection string
def connection_string():
    load_dotenv()
    mongodb_uri = os.getenv("MONGODB_URI")
    connected = MongoClient(mongodb_uri)
    return connected

# get authorization token
def loggedInUser():
    LOGINURL = "http://localhost:4200/api/login"
    payload = {"email": "repro@gmail.com", "password": "repro123456"}

    try:
        response = requests.post(LOGINURL, json=payload)

        if response.status_code == 200:
            data = response.json()
            token = data.get('token', 'N/A')
            return token
        else:
            print(f'Error Code: {response.status_code}\n{response.text}')
            return 'error'
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
        return 'error'


# dictionary for all collection names as keys and extracted form as values
collectionDict = {"movies":"dbpedia_movies1.json", "companies": "dbpedia_companies1.json", "drugs":"dbpedia-drugs1.json"}



