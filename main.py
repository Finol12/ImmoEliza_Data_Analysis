import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
from src import utils

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


