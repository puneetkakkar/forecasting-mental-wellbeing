from flask import current_app as app
from flask.cli import AppGroup, with_appcontext
from utils.db_utils import is_database_connected
from app import initialize_db_with_data

# Here we are defining all the commands related to our db. 

# Create an AppGroup for your DB commands
db_commands_group = AppGroup('dbc', help='Database commands')

# The init command helps in initializing the database 
# with the saved csv results including the predictions 
# fetched from our trained model to the database.
@db_commands_group.command('init')
@with_appcontext
def run_db_data_initialization():
    with app.app_context():
        if is_database_connected():
            initialize_db_with_data()
        else: 
            app.logger.warn('Failed to connect to the database.')



