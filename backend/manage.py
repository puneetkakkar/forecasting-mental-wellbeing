from flask.cli import FlaskGroup
from app import create_app
from app.model import db
from app.model.mental_health_dataset import MentalHealthDataset
from app.model.suicide_rate_predictions import SuicideRatePredictions
from utils.cli_commands import db_commands_group
from flask_migrate import Migrate

app = create_app()

app.logger.warn(f"DB: {db}")

db.init_app(app)
migrate = Migrate(app, db)

# Register flask app commands
app.cli.add_command(db_commands_group)

# Initialize the Flask CLI
cli = FlaskGroup(app)
cli()