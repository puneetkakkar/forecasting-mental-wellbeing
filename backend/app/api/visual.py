import pandas as pd
from flask import Blueprint, request, jsonify
from flask import current_app as app
from app.model.mental_health_dataset import MentalHealthDataset
from app.model.suicide_rate_predictions import SuicideRatePredictions
from app.model import db
from sqlalchemy import and_

visual = Blueprint("visual", __name__, url_prefix='/visual')

@visual.route('/countries-list', methods=['GET'])
def get_predicted_countries_list():
    try:
        results = SuicideRatePredictions.query.with_entities(SuicideRatePredictions.entity, SuicideRatePredictions.predicted_suicide_rate).distinct().all()

        country_names = [country[0] for country in results]
        
        return jsonify({'status': True , 'data': country_names})

    except Exception as e:
        return jsonify({'status': False, "data": [],'error': str(e)})

@visual.route('/similar-countries', methods=['POST'])
def similar_countries_visual():
    try:
        data = request.get_json()
        country_name = data['country']

        results = SuicideRatePredictions.query.with_entities(SuicideRatePredictions.entity, SuicideRatePredictions.predicted_suicide_rate).distinct().all()

        country_names = [country[0] for country in results]

        country_suicide_rates = {country: suicide_rate for country, suicide_rate in results}

        similarity_buffer_threshold = 20

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

        response_data = [{'country': country, 'code': code, 'suicide_rate': suicide_rate * 100} for country, code, suicide_rate in similar_countries_predictions]

        return jsonify({"status": True, "data": response_data})

    except Exception as e:
        return jsonify({'status': False, "data": [], 'error': str(e)})