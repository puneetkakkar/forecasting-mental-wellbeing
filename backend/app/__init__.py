import os
from flask import Flask
from werkzeug.utils import import_string
import pandas as pd
from flask_cors import CORS
from app.model import db
from flask import current_app as app

# Import all the Blueprints used throughout our 
# backend application. These help in breaking our 
# API-endpoints to a modular design.
from app.main import main
from app.api import api
from app.api.predict import predict
from app.api.visual import visual

# Here, we are feeding the pre-saved predictions csv to the database. 
# Before storing it to the database, we perform certain operations such 
# as renaming the columns wihtin the csv to make them compatible to 
# our database schema. Then, pushing the data to the MySQL database.
def initialize_db_with_data():
    engine = db.get_engine()
    connection = engine.connect()

    df = pd.read_csv('data/predictions.csv')

    rename_columns = {
        'Entity':'entity', 'Code':'code', 'Prevalence in females (%)':'prevalence_in_females', 'Prevalence in males (%)':'prevalence_in_males', 'Adult 20-34 years old (%)': 'adult_percentage', 'Old 50-70+ years old (%)': 'old_percentage', 'Young 10-19 years old (%)':'young_percentage', 'Alcohol use disorders (%)': 'alcohol_use_disorders', 'Anxiety disorders (%)':'anxiety_disorders', 'Bipolar disorder (%)':'bipolar_disorder', 'Depression (%)': 'depression', 'Drug use disorders (%)':'drug_use_disorders', 'Schizophrenia (%)':'schizophrenia', 'Eating disorders (%)': 'eating_disorders', 'Depressive disorder rates (number suffering per 100,000)':'depressive_disorder_rates', 'Population': 'country_population', 'Prevalence - Depressive disorders - Sex: Both - Age: All Ages (Number) (people suffering from depression)': 'prevalence_depressive_disorders_sex_both_age_all_ages', 'Suicide Rate Predictions': 'predicted_suicide_rate'
    }

    # Renaming the columns
    df.rename(columns=rename_columns, inplace=True)

    try:
        # Push DataFrame to MySQL database
        df.to_sql('mental_health_dataset', con=connection, if_exists='replace', index=False)
        print('Data pushed to MySQL successfully!')
    except Exception as e:
        print(f'Error pushing data to MySQL: {e}')
    finally:
        # Close the connection in a finally block to ensure it's always closed
        connection.close()

# Here we are wrapping whole of our application to a single function 
# using various flask related utilities. Along with that we are loading 
# all the settings from the environment variables into the application 
# at runtime, and registering all the API related blueprints to our flask application.
def create_app(**config_overrides):
    app = Flask(__name__, instance_relative_config=True)

    # Added a CORS extension to our flask 
    # backend to solve prefligh issues.
    cors = CORS(app)

    app.config.update(config_overrides)

    # Load config
    app.config.from_pyfile('settings.py')

    app.register_blueprint(main)
    api.register_blueprint(predict)
    api.register_blueprint(visual)
    app.register_blueprint(api)

    return app