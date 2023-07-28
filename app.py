from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score
import xgboost as xgb
import pickle
import json





app = FastAPI()

class Feature(BaseModel):
    houseORapartment : str
    Bedroom : int
    Living_area : int
    Swimming_pool : int
    Garden : int
    Garden_area : int
    Surface_of_land : int
    Terrace: int
    Facade : int
    Open_Fire : int
    Furnished : int
    province : str
    District: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/features")
def features(data: Feature):
    # Access the attributes of the Feature object
    data_dict = {
        "Bedroom": data.Bedroom,
        "Living_area": data.Living_area,
        "Swimming_pool": data.Swimming_pool,
        "Garden": data.Garden,
        "Garden_area": data.Garden_area,
        "Surface_of_land": data.Surface_of_land,
        "Terrace": data.Terrace,
        "Facade": data.Facade,
        "Open_Fire": data.Open_Fire,
        "Furnished": data.Furnished,
        "province" : data.province,
        "District" : data.District

    }
    
    # Convert the dictionary to a DataFrame
    df = pd.DataFrame([data_dict])

    filename_province = "./data/encoder_province.pickle"
    province_encoder = pickle.load(open(filename_province, "rb"))
    province_encoded = province_encoder.transform(df[['province']])
    province_df = pd.DataFrame(province_encoded, columns=province_encoder.get_feature_names_out(['province']))
    df = pd.concat([df, province_df], axis=1)
    

    filename_district = "./data/encoder_district.pickle"
    district_encoder = pickle.load(open(filename_district, "rb"))
    district_encoded = district_encoder.transform(df[['District']])
    district_df = pd.DataFrame(district_encoded, columns=district_encoder.get_feature_names_out(['District']))
    df = pd.concat([df, district_df], axis=1)
    

    df = df.drop(['province','District'], axis = 1)


    X_test = df.to_numpy()



    # load model
    if data.houseORapartment=="house":
        filename = "./data/xgb_regressor_house.pickle"
        loaded_model = pickle.load(open(filename, "rb"))
    elif data.houseORapartment=="apartment":
        filename = "./data/xgb_regressor_apartment.pickle"
        loaded_model = pickle.load(open(filename, "rb"))
    # you can use loaded model to compute predictions
    
    y_predicted = loaded_model.predict(X_test)
    # Convert predictions to a JSON-serializable format
    predictions_json = y_predicted.tolist()

    return predictions_json
    






