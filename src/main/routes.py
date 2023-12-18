from logging import info
from flask import Blueprint, request
import os
import pandas as pd
import numpy as np

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    # get request
    return 'Hello World!'

@main.route('/predict', methods=['POST']) 
def predict():
    # user_data = 2d array (1, 43)
    data = request.get_json()
    input = data.get('input_data')

    # load model
    from tensorflow.keras.models import load_model

    models_dir = os.path.join(os.getcwd(), 'models')
    model_file_path = os.path.join(models_dir, 'food_model_1.h5')
    data_file_path = os.path.join(models_dir, 'List_Label.csv')
    
    dataset=pd.read_csv(data_file_path)
    model = load_model(model_file_path)

    # do prediction
    y_pred = model.predict(input)
    top_5 = np.argsort(y_pred.flatten())[-5:]
    selected_rows = dataset.loc[dataset['label'].isin(top_5), ['name', 'label']]
    selected_rows.sort_values(by='label',ascending=True,inplace=True)

    result = selected_rows.drop_duplicates(subset=['label'])

    # return result

    return result.to_json(orient="records"), 200, {'Content-Type': 'application/json'}