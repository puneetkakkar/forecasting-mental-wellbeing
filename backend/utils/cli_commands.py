from flask import current_app as app
from flask.cli import AppGroup, with_appcontext
from utils.db_utils import is_database_connected
from app import initialize_db_with_data

# Create an AppGroup for your DB commands
db_commands_group = AppGroup('dbc', help='Database commands')

@db_commands_group.command('init')
@with_appcontext
def run_db_data_initialization():
    with app.app_context():
        if is_database_connected():
            initialize_db_with_data()
        else: 
            app.logger.warn('Failed to connect to the database.')



