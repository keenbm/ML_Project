import pandas as pd
import dynamicplot
df=pd.read_csv("https://raw.githubusercontent.com/krishnaik06/Advanced-House-Price-Prediction-/master/train.csv")
dynamicplot.cat_num_var_plot(df,target_col="SalePrice",filename="Graph1",path="Graph1")
dynamicplot.num_num_var_plot(df,target_col="SalePrice",filename="Graph2",path="Graph2")
dynamicplot.null_num_var_plot(df,target_col="SalePrice",filename="Graph3",path="Graph3")
dynamicplot.mul_var_plot(df,target_col="SalePrice",filename="Graph7",path="Graph7")


#df=pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")
##dict1={"Survived":"object","Pclass":"object","Sex":"object","SibSp":"object","Parch":"object"}
#df=dynamicplot.convert_dtype(df,dict1)
#dynamicplot.cat_cat_var_plot(df,target_col="Survived",filename="Graph4",path="Graph4")
#dynamicplot.num_cat_var_plot(df,target_col="Survived",filename="Graph5",path="Graph5")
#dynamicplot.null_cat_var_plot(df,target_col="Survived",filename="Graph6",path="Graph6")