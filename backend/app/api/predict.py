import json
import pandas as pd
from flask import Blueprint, request, jsonify
from utils import pkl_loader, util
from flask import current_app as app
from app.model import db

# Defining the predict api-endpoint for our flask backend application.
predict = Blueprint("predict", __name__, url_prefix='/predict')

# Performing the operations required to predict the suicide rates 
# based on the input dataset served to the backend API via the frontend.
@predict.route('/rf', methods=['POST'])
def rf():
    try:
        # Get user input as CSV file
        user_input = request.files['file']
        
        # Read the CSV file into a DataFrame
        input_df = pd.read_csv(user_input)

        # One-hot encoding - Entity and Code
        entity_ohe_mapping, code_ohe_mapping = pkl_loader.load_ohe_mappings()

        # Converting the fetched one-hot encoding mapping values to a list explicitly
        entity_values = list(entity_ohe_mapping.values())
        code_values = list(code_ohe_mapping.values())

        # Filtering the Entities and Code present in our one-hot encoding list
        valid_entity_mask = input_df['Entity'].isin(entity_values)
        valid_code_mask = input_df['Code'].isin(code_values)
        input_df.loc[valid_entity_mask, 'Entity'] = input_df.loc[valid_entity_mask, 'Entity'] \
                                                        .map(lambda entity: util.get_key_from_dict(
                                                            entity_ohe_mapping, entity
                                                        ))
        input_df.loc[valid_code_mask, 'Code'] = input_df.loc[valid_code_mask, 'Code'] \
                                                        .map(lambda code: util.get_key_from_dict(
                                                            code_ohe_mapping, code
                                                        ))

        # Converting the values converted to int explicitly
        input_df['Entity'], input_df['Code'] = input_df['Entity'].astype(int), input_df['Code'].astype(int) 

        # Dropping the target coloumn if present in the database
        input_df = input_df.drop(columns = 'Suicide rate (deaths per 100,000 individuals)')

        # Extract numeric features for normalization (excluding 'Entity' and 'Code')
        numeric_features = input_df.drop(columns=['Entity', 'Code'])

        # Loading the saved min-max scaler transformation
        scaler = pkl_loader.load_min_max_scaler_instance()

        # Normalize only selected features using MinMaxScaler
        input_df[numeric_features.columns] = scaler.transform(numeric_features)

        # Loading trained random forest model
        random_forest_model = pkl_loader.load_rf_model()

        # Make predictions using the Random Forest Model
        predictions = random_forest_model.predict(input_df)

        # Convert predictions to percentage
        predictions_percentage = predictions * 100

        # Add predictions to the DataFrame
        input_df['predicted_suicide_rate'] = predictions_percentage

        # Convert the Entity and Code values to their repective string values (reverse one-hot encoding)
        input_df['Entity'] = input_df['Entity'].replace(entity_ohe_mapping)
        input_df['Code'] = input_df['Code'].replace(code_ohe_mapping)

        rename_columns = {
            'Entity':'entity', 'Code':'code', 'Prevalence in females (%)':'prevalence_in_females', 'Prevalence in males (%)':'prevalence_in_males', 'Adult 20-34 years old (%)': 'adult_percentage', 'Old 50-70+ years old (%)': 'old_percentage', 'Young 10-19 years old (%)':'young_percentage', 'Alcohol use disorders (%)': 'alcohol_use_disorders', 'Anxiety disorders (%)':'anxiety_disorders', 'Bipolar disorder (%)':'bipolar_disorder', 'Depression (%)': 'depression', 'Drug use disorders (%)':'drug_use_disorders', 'Schizophrenia (%)':'schizophrenia', 'Eating disorders (%)': 'eating_disorders', 'Depressive disorder rates (number suffering per 100,000)':'depressive_disorder_rates', 'Population': 'country_population', 'Prevalence - Depressive disorders - Sex: Both - Age: All Ages (Number) (people suffering from depression)': 'prevalence_depressive_disorders_sex_both_age_all_ages'
        }

        # Renaming the columns of the input dataframe to make it compatible 
        # with our database schema model.
        input_df.rename(columns=rename_columns, inplace=True)

        # Converting all the values to percentage values.
        input_df['prevalence_in_males'] = input_df['prevalence_in_males'] * 100
        input_df['prevalence_in_females'] = input_df['prevalence_in_females'] * 100

        input_df['young_percentage'] = input_df['young_percentage'] * 100
        input_df['adult_percentage'] = input_df['adult_percentage'] * 100
        input_df['old_percentage'] = input_df['old_percentage'] * 100

        input_df['alcohol_use_disorders'] = input_df['alcohol_use_disorders'] * 100
        input_df['anxiety_disorders'] = input_df['anxiety_disorders'] * 100
        input_df['bipolar_disorder'] = input_df['bipolar_disorder'] * 100
        input_df['depression'] = input_df['depression'] * 100
        input_df['drug_use_disorders'] = input_df['drug_use_disorders'] * 100
        input_df['schizophrenia'] = input_df['schizophrenia'] * 100
        input_df['eating_disorders'] = input_df['eating_disorders'] * 100

        input_df['depressive_disorder_rates'] = input_df['depressive_disorder_rates'] * 100
        input_df['prevalence_depressive_disorders_sex_both_age_all_ages'] = input_df['prevalence_depressive_disorders_sex_both_age_all_ages'] * 100

        # Grouping our input datafram based on the entity and code.
        group_by_cols = ['entity', 'code']
        input_df = input_df.groupby(group_by_cols)

        input_df = input_df.mean().reset_index()

        # Saving predictions to the database
        with app.app_context():
            engine = db.get_engine()
            connection = engine.connect()
            try:
                # Push DataFrame to MySQL database
                input_df.to_sql('suicide_rate_predictions', con=connection, if_exists='replace', index=False)
                print('Predictions pushed to MySQL successfully!')
            except Exception as e:
                print(f'Error pushing Prediction to MySQL: {e}')
            finally:
                # Close the connection in a finally block to ensure it's always closed
                connection.close()

        # List of columns to drop before sendnig the response back to the client
        final_columns_to_drop = [
            'depressive_disorder_rates', 'country_population', 'prevalence_depressive_disorders_sex_both_age_all_ages'
        ]

        # Dropping the columns that are not to be included while sending the response to the user
        response_df = input_df.drop(columns=final_columns_to_drop)

        # Return the result as JSON
        result = response_df.to_json(orient='records', date_format='iso', compression='gzip')

        data = json.loads(result)

        return jsonify({'status': True, "data": data})

    except Exception as e:
        return jsonify({'status': False, "data": [],'error': str(e)})