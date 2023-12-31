import pandas as pd
import numpy as np 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score
import xgboost as xgb
from sklearn.preprocessing import OneHotEncoder
# library for save and load scikit-learn models
import pickle
# Process and split the input DataFrame into separate DataFrames for apartments and houses
def get_df(df):

    # Convert boolean columns to integers (0 for False and 1 for True)
    df['Swimming_pool'] = df['Swimming_pool'].astype(int)
    df['Garden'] = df['Garden'].astype(int)
    df['Terrace'] = df['Terrace'].astype(int)
    df['Open Fire'] = df['Open Fire'].astype(int)
    df['Furnished'] = df['Furnished'].astype(int)
    # Perform one-hot encoding for the 'province' column
    # df = pd.get_dummies(df, columns=['province','District'])

    # Perform one-hot encoding for the 'province' column
    province_encoder = OneHotEncoder(drop='first', sparse=False)
    province_encoded = province_encoder.fit_transform(df[['province']])
    province_df = pd.DataFrame(province_encoded, columns=province_encoder.get_feature_names_out(['province']))
    df = pd.concat([df, province_df], axis=1)
    
    # Perform one-hot encoding for the 'District' column
    district_encoder = OneHotEncoder(drop='first', sparse=False)
    district_encoded = district_encoder.fit_transform(df[['District']])
    district_df = pd.DataFrame(district_encoded, columns=district_encoder.get_feature_names_out(['District']))
    df = pd.concat([df, district_df], axis=1)

    # file name, I'm using *.pickle as a file extension
    filename_province = "./data/encoder_province.pickle"
    filename_district = "./data/encoder_district.pickle"
    # save encoders
    pickle.dump(province_encoder, open(filename_province, "wb"))
    pickle.dump(district_encoder, open(filename_district, "wb"))

    
    # Filter and process apartment data
    apartment_df = df[df["Type"] == "apartment"]
    columns_to_drop_apartment = ['URL','Listing_ID','province','District','Price_per_sqm','Type', 'Subtype','Listing_address','Postal_code', 'Locality', 'Kitchen','State of the building']
    apartment_df = apartment_df.drop(columns= columns_to_drop_apartment)
    apartment_df.to_csv('./data/apartment_df.csv', index=False)
    # Filter and process house data
    house_df = df[df["Type"] == "house"]
    columns_to_drop_house =  ['URL', 'Listing_ID','Type','province','District','Price_per_sqm','Subtype','Listing_address','Postal_code', 'Locality', 'Kitchen','State of the building']
    house_df = house_df.drop(columns= columns_to_drop_house)
    house_df.to_csv('./data/house_df.csv', index=False)
    # Return the separate DataFrames for apartments and houses
    return apartment_df, house_df


# Train a linear regression model on the input DataFrame.
def train_linear_regression(df, target_col, test_size=0.2, random_state=0):
    # Split the DataFrame into feature matrix (X) and target vector (y)
    X = df.drop(columns=[target_col]).to_numpy()
    y = df[target_col].to_numpy().reshape(-1, 1)
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    # Create a linear regression model
    regressor = LinearRegression()
    # Train the linear regression model using the training data
    regressor.fit(X_train, y_train)
    # Calculate the coefficient of determination (R^2) on the training set
    train_score = regressor.score(X_train, y_train)
    # Calculate the coefficient of determination (R^2) on the test set
    test_score = regressor.score(X_test, y_test)

    return train_score, test_score


def train_DecisionTree_regression(df, target_col, test_size=0.2, random_state=0):
     # Split the DataFrame into feature matrix (X) and target vector (y)
    X = df.drop(columns=[target_col]).to_numpy()
    y = df[target_col].to_numpy().reshape(-1, 1)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    # Train the DecisionTree model 
    dt_regressor = DecisionTreeRegressor()
    # Fit the models to the training data
    dt_regressor.fit(X_train,y_train)
    # Predict on the test data
    y_pred = dt_regressor.predict(X_test)
    # Calculate R-squared for apartment and house models
    r2 = r2_score(y_test, y_pred)
    return r2
    


def train_xgboost_house(df, target_col, test_size=0.2, random_state=0):
    # Split the DataFrame into feature matrix (X) and target vector (y)
    X = df.drop(columns=[target_col]).to_numpy()
    y = df[target_col].to_numpy().reshape(-1, 1)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    # Train the xgboost model 
    xgb_regressor = xgb.XGBRegressor()
    # Fit the models to the training data
    xgb_regressor.fit(X_train,y_train)
    # Predict on the test data
    y_pred = xgb_regressor.predict(X_test)
    # Calculate R-squared for apartment and house models
    r2 = r2_score(y_test, y_pred)

    # save the trained model with pickle
    # file name, I'm using *.pickle as a file extension
    filename = "./data/xgb_regressor_house.pickle"

    # save model
    pickle.dump(xgb_regressor, open(filename, "wb"))
    return r2
   
def train_xgboost_apartment(df, target_col, test_size=0.2, random_state=0):
    # Split the DataFrame into feature matrix (X) and target vector (y)
    X = df.drop(columns=[target_col]).to_numpy()
    y = df[target_col].to_numpy().reshape(-1, 1)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    # Train the xgboost model 
    xgb_regressor = xgb.XGBRegressor()
    # Fit the models to the training data
    xgb_regressor.fit(X_train,y_train)
    # Predict on the test data
    y_pred = xgb_regressor.predict(X_test)
    # Calculate R-squared for apartment and house models
    r2 = r2_score(y_test, y_pred)

    # save the trained model with pickle
    # file name, I'm using *.pickle as a file extension
    filename = "./data/xgb_regressor_apartment.pickle"

    # save model
    pickle.dump(xgb_regressor, open(filename, "wb"))
    return r2


    




    