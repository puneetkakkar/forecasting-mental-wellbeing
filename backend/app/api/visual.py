import pandas as pd
from flask import Blueprint, request, jsonify
from flask import current_app as app
from app.model.mental_health_dataset import MentalHealthDataset
from app.model.suicide_rate_predictions import SuicideRatePredictions
from app.model import db
from sqlalchemy import and_

# Here, we are registering our visual API-endpoint blueprint
visual = Blueprint("visual", __name__, url_prefix='/visual')

# The following API-endpoint provides a unique list of countries 
# based on the input dataset provided by the user.
@visual.route('/countries-list', methods=['GET'])
def get_predicted_countries_list():
    try:
        # This query to the database, fetches country, and their suicide rates and then filter them to 
        # select only distinct countries only.
        results = SuicideRatePredictions.query.with_entities(SuicideRatePredictions.entity, SuicideRatePredictions.predicted_suicide_rate).distinct().all()

        # Converting the returned response to a list
        country_names = [country[0] for country in results]
        
        return jsonify({'status': True , 'data': country_names})

    except Exception as e:
        return jsonify({'status': False, "data": [],'error': str(e)})

# Here, we are finding the similar countries that have lesser suicide rates 
# applicable than the input country name passed to this API. 
@visual.route('/similar-countries', methods=['POST'])
def similar_countries_visual():
    try:
        # Fetching the input value given to the API.
        data = request.get_json()
        country_name = data['country']

        # Here, we are fetching the distinct countries from our current made predictions. 
        results = SuicideRatePredictions.query.with_entities(SuicideRatePredictions.entity, SuicideRatePredictions.predicted_suicide_rate).distinct().all()

        # Converting the returned response from the database to a list of countries.
        country_names = [country[0] for country in results]

        # Making a dictionary including key as country and value as its suicide rate.
        country_suicide_rates = {country: suicide_rate for country, suicide_rate in results}

        # Defining the threshold value for our input country, for 
        # showing countries lesser than the following threshold 
        # value for the selected country given to the API as input
        similarity_buffer_threshold = 20

        # Here, we define our SQL query to fetch countries with 
        # lesser suicide rates from the country given in the input to the API.
        similar_countries_predictions = \
            MentalHealthDataset.query.with_entities(MentalHealthDataset.entity, MentalHealthDataset.code, db.func.MAX(MentalHealthDataset.predicted_suicide_rate).label('max_predicted_suicide_rate')) \
            .group_by(MentalHealthDataset.entity, MentalHealthDataset.code) \
            .filter(MentalHealthDataset.entity not in country_names) \
            .having(and_(
            db.func.MAX(MentalHealthDataset.predicted_suicide_rate) * 100 < country_suicide_rates[country_name],
            db.func.MAX(MentalHealthDataset.predicted_suicide_rate) * 100 > (country_suicide_rates[country_name] - similarity_buffer_threshold)
            )) \
            .order_by('max_predicted_suicide_rate') \
            .limit(5).all()

        # We then, convert the values to percentage values for better visualisation and convert the results to a array list containing dictionary for each country found.
        response_data = [{'country': country, 'code': code, 'suicide_rate': suicide_rate * 100} for country, code, suicide_rate in similar_countries_predictions]

        # Returning the JSON response back to the user.
        return jsonify({"status": True, "data": response_data})

    except Exception as e:
        return jsonify({'status': False, "data": [], 'error': str(e)})