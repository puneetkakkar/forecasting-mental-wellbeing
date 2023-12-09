from sqlalchemy.exc import OperationalError
from app.model import db

def is_database_connected():
    try:
        # Attempt to connect to the database
        connection = db.engine.connect()
        connection.close()
        return True
    except OperationalError:
        return False
