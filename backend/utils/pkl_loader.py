import joblib
import pickle

# Load Random Forest Model
def load_rf_model():
    pkl_file_path = "pkl-files/random_forest_model.pkl"
    random_forest_model = joblib.load(pkl_file_path)
    return random_forest_model

# Load one-hot encoding mapping for 'Entity' and 'Code'
def load_ohe_mappings():
    entitiy_ohe_pkl_file_path = "pkl-files/entity_ohe_mapping.pkl"
    entity_code_ohe_pkl_file_path = "pkl-files/entity_code_ohe_mapping.pkl"

    # Load one-hot encoding mapping for 'Entity'
    entity_encoding_mapping = joblib.load(entitiy_ohe_pkl_file_path)

    # Load one-hot encoding mapping for'Code'
    code_encoding_mapping = joblib.load(entity_code_ohe_pkl_file_path)

    return entity_encoding_mapping, code_encoding_mapping

# Load MinMaxScaler instance
def load_min_max_scaler_instance():
    pkl_file_path = "pkl-files/min_max_scaler.pkl"
    permission = 'rb'
    with open(pkl_file_path, permission) as scaler_file:
        scaler = pickle.load(scaler_file)

    return scaler
    
