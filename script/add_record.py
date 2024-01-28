# pylint: skip-file

"""Insert records into MongoDB"""
import os
import json
import requests
from pymongo import errors
from mdb_required import collectionDict, connection_string

REGISTERURL = "http://localhost:4200/api/register"

def clean_line(line):
    # Remove non-ASCII and invalid control characters, preserving JSON structure
    cleaned_line = ''.join(char if 31 < ord(char) < 127 else ' ' for char in line)
    return cleaned_line

def createUser():
    # add user is user does not already exist
    payload = {"email":"repro@gmail.com","username":"repro","password":"repro123456"}
    try:
        response = requests.post(REGISTERURL, json=payload)

        if response.status_code == 200:
            return 'ok'
        else:
            print(f'Error Code: {response.status_code}\n{response.text}')
            return 'error'
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
        return 'error'

def extract_and_import(collectionName, tar_file_name, extracted_json_folder):
    datasets_folder = "/home/kali/JSONSchemaDiscovery/datasets/" + collectionName 
    tar_file = os.path.join(datasets_folder, tar_file_name + ".tar.bz2")

    # Extract the tar.bz2 file
    # saved the extracted json inside the dataset folder
    extract_command = f'tar -xvjf {tar_file} -C {extracted_json_folder}'
    os.system(extract_command)

    # Connect to MongoDB and create a new collection
    client = connection_string()
    mydb = client.jsonschemadiscovery
    testdata = mydb[collectionName]

    folder_tar_file_name = extracted_json_folder + tar_file_name

    # Import into MongoDB using pymongo
    # tarfilename show also come from extracted filepath
    with open(folder_tar_file_name, 'r') as file:
        try:
            for line_number, line in enumerate(file, start=1):
                try:
                    cleaned_line = clean_line(line)
                    data = json.loads(cleaned_line)
                    testdata.insert_one(data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON at line {line_number}: {e}")
            print(f"\nImport Files for {collectionName} completed ...")
        except errors.PyMongoError as e:
            print(f"Error importing data to MongoDB: {e}")

    # Close the MongoDB connection
    client.close()

if __name__ == "__main__":
    # create user
    msglog = createUser()

    if(msglog == 'ok'):
        # Create the extraction folder for json records
        extracted_json_folder = "/home/kali/JSONSchemaDiscovery/datasets/extractedJson/"
        os.makedirs(extracted_json_folder, exist_ok=True)
        # Automate the process to run for all collections [movies, companies, drugs]
        for collectionName, tar_file_name in collectionDict.items():
            extract_and_import(collectionName, tar_file_name, extracted_json_folder)
    