"""Drop database"""
from mdb_required import connection_string

def remove_db():
    client = connection_string()
    client.drop_database("jsonschemadiscovery")
    client.close()

if __name__ == "__main__":
    remove_db()
