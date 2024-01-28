"""Extract JSON schemas"""
import requests
from mdb_required import collectionDict
from mdb_header import HEADER

AUTHENTICATION = {
    'authMechanism': 'SCRAM-SHA-1',
    'userName': 'mongoadmin',
    'password': 'secret',
    'authDatabase': 'admin'
}

def send_request_to_server(collection_name):
    """Send a POST request to the server to extract raw schema for a given collection."""
    POST_URL = 'http://localhost:4200/api/batch/rawschema/steps/all'
    payload = {
        'authentication': AUTHENTICATION,
        'port': '27017',
        'address': 'mongodb',
        'databaseName': 'jsonschemadiscovery',
        'collectionName': collection_name
    }

    try:
        response = requests.post(POST_URL, json=payload, headers=HEADER)

        if response.status_code == 200:
            return 'ok'
        else:
            print(f'Error Code: {response.status_code}\n{response.text}')
            return 'error'
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
        return 'error'

def show_analysis():
    """Retrieve and analyze batch data from the server."""
    schema_results = []
    GET_URL = 'http://localhost:4200/api/batches'
    try:
        response = requests.get(GET_URL, headers=HEADER)

        if response.status_code == 200:
            data = response.json()

            for result in data:
                # Extract relevant information from the server response
                collection_name = result.get('collectionName', 'N/A')
                collection_count = result.get('collectionCount', 'N/A')
                batch_id = result.get('_id', 'N/A')
                ordered_field = result.get('uniqueOrderedCount', 'N/A')
                unordered_field = result.get('uniqueUnorderedCount', 'N/A')
                
                # Create a dictionary with the extracted information
                result_dict = {
                    '_id': batch_id,
                    'collectionName': collection_name,
                    'collectionCount': collection_count,
                    'uniqueUnorderedCount': unordered_field,
                    'uniqueOrderedCount': ordered_field
                }

                schema_results.append(result_dict)
            
            return schema_results
        else:
            return f'Failed to retrieve data. Status Code: {response.status_code}'

    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')

if __name__ == '__main__':
    # List of collections to send requests for
    collection_names = list(collectionDict.keys())

    # Iterate over collection_names and send data to the server
    for collectionName in collection_names:
        send_data = send_request_to_server(collectionName)

    # Analyze the retrieved data
    analyzedResult = show_analysis()
    print(analyzedResult)