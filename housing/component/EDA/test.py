import pandas as pd
import dynamicplot
import staticplot

df=pd.read_csv("https://raw.githubusercontent.com/krishnaik06/Advanced-House-Price-Prediction-/master/train.csv")

year_feature=[feature for feature in df if 'Yr' in feature or 'Year' in feature]
dynamicplot.temporal_cat_var_plot(df,target_col="SaleType",temporal_var_list=year_feature,filename="Graph11",path="Graph11")
