"""logged in user header file"""
from mdb_required import loggedInUser

# header for request
HEADER = {
    "content-type": "application/json",
    "Authorization": f"Bearer {loggedInUser()}"
}