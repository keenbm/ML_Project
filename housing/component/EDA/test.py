import dynamicplot
import pandas as pd

df=pd.read_csv("https://raw.githubusercontent.com/krishnaik06/Advanced-House-Price-Prediction-/master/train.csv")
dynamicplot.PandaProfile_report(df,target_col="SalePrice",filename="Graph9",path="Graph9",minimal_ip=False)