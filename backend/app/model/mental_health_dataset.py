from . import db
from . import AppModel

# It includes the schema for our input mental health dataset which 
# includes all the predictions made by our trained model.
class MentalHealthDataset(AppModel):
    id = db.Column(db.Integer, primary_key=True)
    entity = db.Column(db.String(50))
    code = db.Column(db.String(10))
    schizophrenia = db.Column(db.Integer)
    bipolar_disorder = db.Column(db.Integer)
    eating_disorders = db.Column(db.Integer)
    anxiety_disorders = db.Column(db.Integer)
    drug_use_disorders = db.Column(db.Integer)
    depression = db.Column(db.Integer)
    alcohol_use_disorders = db.Column(db.Integer)
    prevalence_in_males = db.Column(db.Integer)
    prevalence_in_females = db.Column(db.Integer)
    country_population = db.Column(db.BigInteger)
    predicted_suicide_rate = db.Column(db.Integer)
    depressive_disorder_rates = db.Column(db.Integer)
    prevalence_depressive_disorders_sex_both_age_all_ages = db.Column(db.Integer)
    young_percentage = db.Column(db.Integer)
    adult_percentage = db.Column(db.Integer)
    old_percentage = db.Column(db.Integer)

    def __init__(self, country):
        self.country = country

    def __repr__(self):
        return '<Country %r>' % self.country
