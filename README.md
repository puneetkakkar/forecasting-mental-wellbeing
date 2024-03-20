# Forecasting Mental Wellbeing: A Suicide Predictor and Mental Health Problems

We have developed a predictive model using random forest regressor to estimate suicide rates on a county basis, taking into account the prevalence of mental disorders, age demographics and gender distribution. We aim to assist public health agencies and policy makrs to tailor their efforts in order to curb the suicide rates. 


![dic](https://github.com/puneetkakkar/forecasting-mental-wellbeing/assets/47149740/9471d74c-634a-4de8-a1d1-d40fc44e0b1e)


## Installation

- Install [Docker] as a pre-requisite to run the project.

```bash
# Clone Forecasting-Mental-Wellbeing Repository
git clone https://github.com/puneetkakkar/forecasting-mental-wellbeing.git

# Navigate to project directory
cd forecasting-mental-wellbeing

# To start the project execute the start script
sh ./start.sh

# Run DB migrations i.e., initialize the db and its schema 
# based on models definied.
docker exec –it mental-wellbeing-api flask db init

# Store the DB migrations command to run within the 
# database as per the models defined in the cod
docker exec –it mental-wellbeing-api flask db migrate

# Apply the stored migrations to the MySQL database.
docker exec –it mental-wellbeing-api flask db upgrade

# Once the db migrations are completed, enter the following
# command to populate data within the database.
docker exec –it mental-wellbeing-api flask dbc init

# To stop the dockers and stop the project, execute the stop script
sh ./stop.sh
```

[Docker]: https://docs.docker.com/get-docker/