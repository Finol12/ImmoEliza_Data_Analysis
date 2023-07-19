import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score
import xgboost as xgb

from src import utils
from src import ML

utils.cleaning_data("./data/raw-data.csv")

df = pd.read_csv("./data/cleaned_data.csv")

utils.PlotBar_1(df)
utils.PlotBar_2(df)
utils.Heatmap(df)
utils.Price_hist(df)
utils.Price_log(df)
utils.Regression(df)
utils.Furnished_Price_boxplot(df)
utils.Garden_boxplot(df)
utils.Swimming_pool_boxplot(df)
utils.Furnished_Area(df)
utils.Price_by_province_boxplot(df)
utils.house_apartment_hist(df)
utils.house_and_partment_price_per_sqm(df)


apartment_df, house_df=ML.get_df(df)


##Linear Regression model
train_score_apartment, test_score_apartment=ML.train_linear_regression(apartment_df, "Price", test_size=0.2, random_state=0)
train_score_house, test_score_house=ML.train_linear_regression(house_df, "Price", test_size=0.2, random_state=0)
print("train_score_apartment:  ",train_score_apartment)
print("test_score_apartment:  ",test_score_apartment)

print("train_score_house:  ",train_score_house)
print("test_score_house:  ",test_score_house)


####DecisionTRee model
r2_apartment=ML.train_DecisionTree_regression(apartment_df, "Price", test_size=0.2, random_state=0)
r2_house=ML.train_DecisionTree_regression(house_df, "Price", test_size=0.2, random_state=0)

print("DecisionTRee R-squared (Apartment):", r2_apartment)
print("DecisionTRee R-squared (House):", r2_house)


####xgboost model
r2_apartment=ML.train_xgboost(apartment_df, "Price", test_size=0.2, random_state=0)
r2_house=ML.train_xgboost(house_df, "Price", test_size=0.2, random_state=0)

print("xgboost R-squared (Apartment):", r2_apartment)
print("xgboost R-squared (House):", r2_house)