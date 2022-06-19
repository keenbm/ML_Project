import pandas as pd
import numpy as np
from scipy import stats 
import numpy as np
import plotly
import plotly.express as px
import plotly.io as pio

from datetime import datetime
import pytz
import time
import os

from housing.logger import logging
from housing.exception import HousingException
import sys


def convert_dtype(input_df,input_dict):
    """
    Use : Change data type as per requirement
    Return : DataFrame with corrected dType
    """
    output_df = input_df.astype(input_dict,)
    return output_df



def html_handler(input_str,filename,folder_name):
    """
    Use : Create / Update HTML file
    Return : None
    """ 
    logging.info(f"html_handler Called to Create/Update : {folder_name}/{filename}.html")
    try:
        with open(f"{folder_name}/{filename}.html",'a') as file:
            file.write(f"<h2 align ='center' style='color:red'> {input_str} </h2>")
            file.write("""<form> <input type="button" value="Go back!" onclick="history.back()"> </form>""")
    except Exception as e:
        housing = HousingException(e,sys)
        logging.info(housing.error_message)    
    return None



def plotly_to_html(fig,filename,folder_name):
    """
    Use : Store Plotly plot HTML file
    Return : None
    """
    logging.info(f"plotly_to_html Called to add plot in {folder_name}/{filename}.html")
    try:
        with open(f"{folder_name}/{filename}.html", 'a') as f:
            f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    except Exception as e:
        housing = HousingException(e,sys)
        logging.info(housing.error_message) 

    return None



def html_create_index(input_str,filename,folder_name):
    """
    Use : Create index file for all the plotly plot
    Return : None
    """    
    logging.info(f"html_create_index call to create {folder_name}/{filename}.html")
    
    try:
        with open(f"{folder_name}/{filename}.html",'a') as file:
            file.write(f"<h1 align ='center' style='color:red'> {input_str} </h1>")

        for f in os.listdir(folder_name):
            if f.endswith('.html') and f!=f"{filename}.html":
                with open(f"{folder_name}/{filename}.html",'a') as file:
                    file.write(f"<li><a href={f}>{f}</a></li>")
            else:
                pass

    except Exception as e:
        housing = HousingException(e,sys)
        logging.info(housing.error_message) 

    return None


##*****************************************************************************************  
## ************************* Function for Numerical Target Variavble ************************


## ******Categorical Vs. Numerical Target variable
def cat_num_var_plot(df,target_col,filename="Graph1",path="Graph1"):
    """
    Use : Create HTML Plot file for
    Categorical Vs. Numerical Target Variable
    Return : None
    """
    logging.info("cat_num_var_plot : Called")
    if not os.path.exists(path):
        os.makedirs(path) 

    categorical_var_list=df.select_dtypes(include=["object"])

    try:
        for column in categorical_var_list:
            html_handler(input_str=column,filename=column,folder_name=path)
            inp_df=df.groupby(column)[target_col].agg(['mean','median','count']).reset_index().rename(columns={'mean': f'Mean : {target_col}','median':f'Median : {target_col}','count':f'{column} : Count'})

            try:
                logging.info(f"Ploting cat_num_var_plot : Fig1 for {column}")
                fig1 = px.bar(inp_df, x=column, y=f'{column} : Count',color=column,
                    barmode="group",title=f'{column} : Count Plot')
                fig1=fig1.update_layout(title_x=0.5,title_font_family="Times New Roman",
                                        title_font_color="black",title_font_size=20)
                plotly_to_html(fig=fig1,filename=column,folder_name=path)
            except Exception as e:
                housing = HousingException(e,sys)
                logging.info(housing.error_message)
                 
           
            try:
                logging.info(f"Ploting cat_num_var_plot : Fig2 for {column}")
                fig2=px.pie(inp_df, values=f'{column} : Count', names=column, title=f'{column} : Pie Chart')
                fig2=fig2.update_traces(textposition='inside', textinfo='percent+label')
                fig2=fig2.update_layout(title_x=0.5,title_font_family="Times New Roman",title_font_color="black",
                                title_font_size=20)
                plotly_to_html(fig=fig2,filename=column,folder_name=path)
            except Exception as e:
                housing = HousingException(e,sys)
                logging.info(housing.error_message)

            try:
                logging.info(f"Ploting cat_num_var_plot : Fig3 for {column}")
                fig3 = px.bar(inp_df, x=column, 
                            y=[f'Mean : {target_col}',f'Median : {target_col}'],
                            barmode="group",title=f'{target_col} Mean & Median Plot')
                fig3=fig3.update_layout(title_x=0.5,title_font_family="Times New Roman",title_font_color="black",
                                title_font_size=20)
                plotly_to_html(fig=fig3,filename=column,folder_name=path)
            except Exception as e:
                housing = HousingException(e,sys)
                logging.info(housing.error_message)

            try:
                logging.info(f"Ploting cat_num_var_plot : Fig4 for {column}")
                fig4 = px.box(df, y=target_col,x=column,notched=True,
                            title=f'{target_col} : Box plot',
                            points="all",color=column)
                fig4=fig4.update_layout(title_x=0.5,title_font_family="Times New Roman",title_font_color="black",
                        title_font_size=20)
                plotly_to_html(fig=fig4,filename=column,folder_name=path)
            except Exception as e:
                housing = HousingException(e,sys)
                logging.info(housing.error_message)

    except Exception as e:
        housing = HousingException(e,sys)
        logging.info(housing.error_message)

    html_create_index(input_str="Categorical Variable Analysis",filename="Graph1",folder_name=path)
    logging.info(f"cat_num_var_plot : Index {path}/{filename}.html Created")
    return None

## ******Numerical Vs. Numerical Target variable
def num_num_var_plot(df,target_col,filename="Graph2",path="Graph2"):
    """
    Use : Create HTML Plot file for
    Numerical Vs. Numerical Target Variable
    Return : None
    """
    logging.info("num_num_var_plot : Called")
    if not os.path.exists(path):
        os.makedirs(path) 
        numerical_var_list=df.select_dtypes(exclude=["object"])

    try:
        for column in numerical_var_list:
            html_handler(input_str=column,filename=column,folder_name=path) 
            
            try:
                logging.info(f"Ploting num_num_var_plot : Fig1 for {column}")
                fig1=px.histogram(df, x=column,marginal="violin",
                                    hover_data=df.columns,title=f'{column} : Histogram Plot')
                fig1=fig1.update_layout(title_x=0.5,title_font_family="Times New Roman",
                                        title_font_color="black",title_font_size=20)
                plotly_to_html(fig=fig1,filename=column,folder_name=path)
            except Exception as e:
                housing = HousingException(e,sys)
                logging.info(housing.error_message)

            try:
                logging.info(f"Ploting num_num_var_plot : Fig2 for {column}")
                fig2=px.violin(df, x=column, points='all', box=True,title=f'{column} : Violin Plot')
                fig2=fig2.update_layout(title_x=0.5,title_font_family="Times New Roman",
                                title_font_color="black",title_font_size=20)
                plotly_to_html(fig=fig2,filename=column,folder_name=path)
            except Exception as e:
                housing = HousingException(e,sys)
                logging.info(housing.error_message)

            try:
                logging.info(f"Ploting num_num_var_plot : Fig3 for {column}")
                fig3 = px.scatter(df, x=column, y=target_col, trendline="ols",
                                    title=f'{column} Vs. {target_col} Reg./Scatter Plot')
                fig3=fig3.update_layout(title_x=0.5,title_font_family="Times New Roman",
                                title_font_color="black",title_font_size=20)
                plotly_to_html(fig=fig3,filename=column,folder_name=path)
            except Exception as e:
                housing = HousingException(e,sys)
                logging.info(housing.error_message)
    
    except Exception as e:
                housing = HousingException(e,sys)
                logging.info(housing.error_message)

    html_create_index(input_str="Numerical Variable Analysis",filename="Graph2",folder_name=path)
    logging.info(f"num_num_var_plot : Index {path}/{filename}.html Created")

    return None

## ******Null Vs. Numerical Target variable

def null_num_var_plot(df,target_col,filename="Graph3",path="Graph3"):
    """
    Use : Create HTML Plot file for
    Null Vs. Numerical Target Variable
    Return : None
    """
    logging.info("null_num_var_plot : Called")
    if not os.path.exists(path):
        os.makedirs(path)

    null_var_list=df.columns[df.isnull().any()].tolist()
    null_var_list.append(target_col)
    null_df=df[null_var_list]

    try:
        for column in null_df.iloc[:,:-1]:
            
            html_handler(input_str=column,filename=column,folder_name=path)

            null_df[column]=np.where(null_df[column].isnull(),"Null","Not Null")
            inp_df=null_df.groupby(column)[target_col].agg(['mean','median','count']).reset_index().rename(columns={'mean': f'Mean : {target_col}','median':f'Median : {target_col}','count':f'{column} : Count'})
            
            try:
                logging.info(f"Ploting null_num_var_plot : Fig1 for {column}")
                fig1 = px.bar(inp_df, x=column, y=f'{column} : Count',color=column,
                        barmode="group",title=f'{column} : Null Value Count Plot')
                fig1=fig1.update_layout(title_x=0.5,title_font_family="Times New Roman",
                                        title_font_color="black", title_font_size=15)
                plotly_to_html(fig=fig1,filename=column,folder_name=path)
            except Exception as e:
                housing = HousingException(e,sys)
                logging.info(housing.error_message)


            try:
                logging.info(f"Ploting null_num_var_plot : Fig2 for {column}")
                fig2=px.pie(inp_df, values=f'{column} : Count', names=column, title=f'{column} :Null Value Pie Chart')
                fig2=fig2.update_traces(textposition='inside', textinfo='percent+label')
                fig2=fig2.update_layout(title_x=0.5,title_font_family="Times New Roman",title_font_color="black",
                            title_font_size=15)
                plotly_to_html(fig=fig2,filename=column,folder_name=path)
            except Exception as e:
                housing = HousingException(e,sys)
                logging.info(housing.error_message)

            try:
                logging.info(f"Ploting null_num_var_plot : Fig3 for {column}")
                fig3 = px.bar(inp_df, x=column, y=[f'Mean : {target_col}',f'Median : {target_col}'],
                                            barmode="group",title=f'{target_col} Null Val. Mean & Median Plot')
                fig3=fig3.update_layout(title_x=0.5,title_font_family="Times New Roman",title_font_color="black",
                            title_font_size=15)
                plotly_to_html(fig=fig3,filename=column,folder_name=path)
            except Exception as e:
                housing = HousingException(e,sys)
                logging.info(housing.error_message)
                
    except Exception as e:
            housing = HousingException(e,sys)
            logging.info(housing.error_message)
        
    html_create_index(input_str="Null Value Analysis",filename="Graph3",folder_name=path)
    logging.info(f"cat_num_var_plot : Index {path}/{filename}.html Created")

    return None


##*****************************************************************************************  
## ************************* Function for Categorical Target Variavble ************************


## ******Categorical Vs. Categorical Target variable

def cat_cat_var_plot(df,target_col,filename="Graph4",path="Graph4"):
    """
    Use : Create HTML Plot file for
    Categorical Vs. Categorical Target Variable
    Return : None
    """
    logging.info("cat_cat_var_plot : Called")
    if not os.path.exists(path):
        os.makedirs(path) 
    categorical_var_list=df.select_dtypes(include=["object"])

    try:
        for column in categorical_var_list:
            html_handler(input_str=column,filename=column,folder_name=path)
            inp_df=df.groupby(column)[target_col].count().reset_index(name=f'{column} : Count')
            
            try:
                logging.info(f"Ploting cat_cat_var_plot : Fig1 for {column}")
                fig1 = px.bar(inp_df, x=column, y=f'{column} : Count',color=column,
                        barmode="group",title=f'{column} : Count Plot')
                fig1=fig1.update_layout(title_x=0.5,
                                        title_font_family="Times New Roman",
                                        title_font_color="black",title_font_size=20)       
                plotly_to_html(fig=fig1,filename=column,folder_name=path)
            except Exception as e:
                housing = HousingException(e,sys)
                logging.info(housing.error_message)

            try:
                logging.info(f"Ploting cat_cat_var_plot : Fig3 for {column}")
                inp_df=df.groupby([target_col,column])[[target_col]].count().rename(columns={target_col:f"{target_col}_count"})
                inp_df=inp_df.reset_index()
                fig2 = px.bar(inp_df, x=target_col, 
                                y=f'{target_col}_count',color=column,
                                barmode="group",title=f'{column} :Stacked Count Plot')
                fig2=fig2.update_layout(title_x=0.5,title_font_family="Times New Roman",
                                        title_font_color="black",title_font_size=20)
                plotly_to_html(fig=fig2,filename=column,folder_name=path)
            except Exception as e:
                housing = HousingException(e,sys)
                logging.info(housing.error_message)

            try:
                logging.info(f"Ploting cat_cat_var_plot : Fig3 for {column}")
                inp_df=df.groupby(column)[target_col].count().reset_index(name=f'{column} : Count')
                fig3=px.pie(inp_df, values=f'{column} : Count', names=column, title=f'{column} : Pie Chart')
                fig3=fig3.update_traces(textposition='inside', textinfo='percent+label')
                fig3=fig3.update_layout(title_x=0.5,title_font_family="Times New Roman",title_font_color="black",
                            title_font_size=20)
                plotly_to_html(fig=fig3,filename=column,folder_name=path)
            except Exception as e:
                housing = HousingException(e,sys)
                logging.info(housing.error_message)            

    except Exception as e:
                housing = HousingException(e,sys)
                logging.info(housing.error_message)

    html_create_index(input_str="Categorical Variable Analysis",filename="Graph4",folder_name=path)
    logging.info(f"cat_cat_var_plot : Index {path}/{filename}.html Created")
    return None

## ******Numerical Vs. Categorical Target variable

def num_cat_var_plot(df,target_col,filename="Graph5",path="Graph5"):
    """
    Use : Create HTML Plot file for
    Numerical Vs. Categorical Target Variable
    Return : None
    """
    logging.info("num_cat_var_plot : Called")
    if not os.path.exists(path):
        os.makedirs(path) 
    numerical_var_list=df.select_dtypes(exclude=["object"])

    try:
        for column in numerical_var_list:
            
            html_handler(input_str=column,filename=column,folder_name=path)
            try:
                logging.info(f"Ploting num_cat_var_plot : Fig1 for {column}")
                fig1=px.histogram(df, x=column,marginal="violin",
                                    hover_data=df.columns,title=f'{column} : Histogram Plot')
                fig1=fig1.update_layout(title_x=0.5,title_font_family="Times New Roman",
                                        title_font_color="black",title_font_size=20)        
                plotly_to_html(fig=fig1,filename=column,folder_name=path)
            except Exception as e:
                housing = HousingException(e,sys)
                logging.info(housing.error_message)

            try:
                logging.info(f"Ploting num_cat_var_plot : Fig2 for {column}")
                fig2=px.violin(df, y=column, points='all', box=True,title=f'{column} : Violin Plot')
                fig2=fig2.update_layout(title_x=0.5,title_font_family="Times New Roman",
                                title_font_color="black",title_font_size=20)
                plotly_to_html(fig=fig2,filename=column,folder_name=path)
            except Exception as e:
                housing = HousingException(e,sys)
                logging.info(housing.error_message)

            try:
                logging.info(f"Ploting num_cat_var_plot : Fig3 for {column}")
                fig3=px.violin(df, x=target_col,y=column,color=target_col, points='all', box=True,title=f'{column} : Violin Plot')
                fig3=fig3.update_layout(title_x=0.5,title_font_family="Times New Roman",
                                title_font_color="black",title_font_size=20)        
                plotly_to_html(fig=fig3,filename=column,folder_name=path)
            except Exception as e:
                housing = HousingException(e,sys)
                logging.info(housing.error_message)

            try:
                logging.info(f"Ploting num_cat_var_plot : Fig4 for {column}")
                inp_df=df.groupby(target_col)[column].agg(["mean","median"]).reset_index().rename(columns={'mean': f'Mean : {column}','median':f'Median : {column}'})
                fig4 = px.bar(inp_df, x=target_col, y=[f'Mean : {column}',f'Median : {column}'],
                        barmode="group",title=f'{column} : Mean Plot')
                fig4=fig4.update_layout(title_x=0.5,title_font_family="Times New Roman",
                                        title_font_color="black",title_font_size=20)
                plotly_to_html(fig=fig4,filename=column,folder_name=path) 
            except Exception as e:
                housing = HousingException(e,sys)
                logging.info(housing.error_message)

    except Exception as e:
                housing = HousingException(e,sys)
                logging.info(housing.error_message)
    
    html_create_index(input_str="Numerical Variable Analysis",filename="Graph5",folder_name=path)
    logging.info(f"num_cat_var_plot : Index {path}/{filename}.html Created")

    return None
    

## ******Null Vs. Categorical Target variable
def null_cat_var_plot(df,target_col,filename="Graph6",path="Graph6"):
    """
    Use : Create HTML Plot file for
    Null Vs. Categorical Target Variable
    Return : None
    """
    logging.info("null_cat_var_plot : Called")

    if not os.path.exists(path):
        os.makedirs(path)

    null_var_list=df.columns[df.isnull().any()].tolist()
    null_var_list.append(target_col)
    null_df=df[null_var_list]
    try:
        for column in null_df.iloc[:,:-1]:
            
            html_handler(input_str=column,filename=column,folder_name=path)

            null_df[column]=np.where(null_df[column].isnull(),"Null","Not Null")
            inp_df=null_df.groupby(column)[target_col].count().reset_index()

            try:
                logging.info(f"Ploting null_cat_var_plot : Fig1 for {column}")
                fig1 = px.bar(inp_df, x=column, y=target_col,color=column,
                                barmode="group",title=f'{column} : Null Value Count Plot')
                fig1=fig1.update_layout(title_x=0.5,title_font_family="Times New Roman",
                                title_font_color="black", title_font_size=15)
                plotly_to_html(fig=fig1,filename=column,folder_name=path)
            except Exception as e:
                    housing = HousingException(e,sys)
                    logging.info(housing.error_message)

    except Exception as e:
                    housing = HousingException(e,sys)
                    logging.info(housing.error_message)
    
    html_create_index(input_str="Null Value Analysis",filename="Graph6",folder_name=path)
    logging.info(f"null_cat_var_plot : Index {path}/{filename}.html Created")

##*****************************************************************************************  
## ************************* Multivariate Analysis ************************

def mul_var_plot(df,target_col,filename="Graph7",path="Graph7"):
    """
    Use : Create HTML Plot file for
    Multivariate Analysis
    Return : None
    """
    logging.info("mul_var_plot : Called")
    if not os.path.exists(path):
        os.makedirs(path) 

    html_handler(input_str=f"Multivariate Analysis : Target Variable {target_col}",filename=filename,folder_name=path)

    numerical_var_list=df.select_dtypes(exclude=["object"])
    corr_df = df.corr()
    corrSale_df=pd.DataFrame(corr_df[target_col])
    corrSale_df.reset_index(inplace=True)
    corrSale_df.sort_values(by=target_col,ascending=True,inplace=True)
    corrSale_df.dropna(inplace=True)
    corrSale_df.columns=["Feature","Pearson_Corr"]

    try:
        logging.info(f"Ploting mul_var_plot : Fig1")
        fig1 = px.bar(corrSale_df, y="Feature", x="Pearson_Corr",
                        color="Pearson_Corr",
                        barmode="group",
                        title=f'Correlation Plot-1 : Target Variable {target_col}')
        fig1=fig1.update_layout(title_x=0.5,
                                title_font_family="Times New Roman",
                                title_font_color="black",
                                title_font_size=20)
        plotly_to_html(fig=fig1,filename=filename,folder_name=path)
    except Exception as e:
        housing = HousingException(e,sys)
        logging.info(housing.error_message)

    try:
        logging.info(f"Ploting mul_var_plot : Fig2")
        fig2=px.imshow(corr_df, text_auto=True, 
                        aspect="auto",
                        title=f'Correlation Plot-2 : Target Variable {target_col}')
        fig2=fig2.update_layout(title_x=0.5,
                            title_font_family="Times New Roman",
                            title_font_color="black",
                            title_font_size=20)
        plotly_to_html(fig=fig2,filename=filename,folder_name=path)
    except Exception as e:
        housing = HousingException(e,sys)
        logging.info(housing.error_message)