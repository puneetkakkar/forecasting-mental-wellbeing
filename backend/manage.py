from flask.cli import FlaskGroup
from app import create_app
from app.model import db
from app.model.mental_health_dataset import MentalHealthDataset
from app.model.suicide_rate_predictions import SuicideRatePredictions
from utils.cli_commands import db_commands_group
from flask_migrate import Migrate

# We are initiating the python flask application here, and 
# binding the whole application by the utility function 
# provided by the flask framework.

app = create_app()

# Initiating our SQLAlchemy extension used for our DB 
# connection within the flask application. This helps in 
# running the migrations and creating the tables as defined 
# in the models files of the applicaiton.
db.init_app(app)
migrate = Migrate(app, db)

# Registering the custom-made flask app commands
app.cli.add_command(db_commands_group)

# Initialize the Flask CLI for the 
# execution of custom-made flask commands
cli = FlaskGroup(app)
cli()