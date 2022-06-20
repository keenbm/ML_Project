import pandas as pd
import numpy as np
from scipy import stats

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import style
import seaborn as sns

from datetime import datetime
import pytz

from housing.logger import logging
from housing.exception import HousingException
import sys
import os

def convert_dtype(input_df,input_dict):
    """
    Use : Change data type as per requirement
    Return : DataFrame with corrected dType
    """
    output_df = input_df.astype(input_dict,)
    return output_df

def plot_size(graphsize):
    """
    Use : Plot size selection
    Return : Plot/Fig. Size
    """
    ## (Width*Height)
    if graphsize=="A4":
        fig_size=(11,8.5)
    elif graphsize=="A3" :
        fig_size=(16.5,12)
    elif graphsize=="mid":
        fig_size=(24,14)
    elif graphsize=="big":
        fig_size=(30,17.5)
    else:
        fig_size=(30,17.5) # By-Default big size
    
    return fig_size


##*****************************************************************************************  
## ************************* Function for Numerical Target Variavble **********************

## ******Categorical Vs. Numerical Target variable
def cat_num_var_plot(df,target_col,graphsize="big",plot_style="ggplot"):
    """
    Use : Create PDF Plot file for
    Categorical Vs. Numerical Target Variable
    Return : None

    Graphsize=A4,A3,mid,big default=big
    #print(plt.style.available)
    """
    logging.info("cat_num_var_plot : Called")
    
    style.use(plot_style)
    
    path="StaticPlot"

    if not os.path.exists(path):
        os.makedirs(path)

    pdf_file_name= f"{path}/cat_num_var_plot" + datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d-%m-%y_%H%M") + ".pdf"   
    graph_pdf = PdfPages(pdf_file_name)
    logging.info(f"Creatin PDF File : {pdf_file_name}")

    
    
    try:
        categorical_var_list=df.select_dtypes(include=["object"])
        for column in categorical_var_list:
            work_figure = plt.figure(constrained_layout=False, figsize=plot_size(graphsize))
            grid = gridspec.GridSpec(ncols=2, nrows=2, figure=work_figure)
            
            try:
                logging.info(f"Ploting cat_num_var_plot : ax1 for {column}")
                ax1 = work_figure.add_subplot(grid[0,0])
                ax1.set_title(column.upper() + ' : Count Plot')
                sns.countplot(x=column,data = df,
                            order = df[column].value_counts().index,ax = ax1)
                plt.xticks(rotation=90)
                for p in ax1.patches:
                    ax1.annotate('{:.0f}'.format(p.get_height()),(p.get_x()+0.2, p.get_height()+2))
            except Exception as e:
                logging.exception(str(e))

            try:
                logging.info(f"Ploting cat_num_var_plot : ax2 for {column}")
                ax2 = work_figure.add_subplot(grid[1, 0])
                ax2.set_title(column.upper() + ' : Box Plot ')
                sns.boxplot(x=column, y= target_col, data = df,
                            order = df[column].value_counts().index,ax=ax2)
                plt.xticks(rotation=90)
            except Exception as e:
                logging.exception(str(e))

            try:
                logging.info(f"Ploting cat_num_var_plot : ax3 for {column}")      
                ax3 = work_figure.add_subplot(grid[:, 1])
                df[column].value_counts().plot.pie(autopct = "%2.2f%%", ax=ax3)
                ax3.set_title(column.upper() + ' : Pie Plot')
            except Exception as e:
                logging.exception(str(e))

            work_figure.tight_layout()
            #plt.show()
            logging.info(f"Saving cat_num_var_plot in PDF for : {column}")
            graph_pdf.savefig(work_figure)
             

    except Exception as e:
                logging.exception(str(e))

    graph_pdf.close()

    return None


## ******Numerical Vs. Numerical Target variable
def num_num_var_plot(df,target_col,graphsize="big",plot_style="ggplot"):
    """
    Use : Create PDF Plot file for
    Numerical Vs. Numerical Target Variable
    Return : None

    Graphsize=A4,A3,mid,big default=big
    #print(plt.style.available)
    """
    logging.info("num_num_var_plot : Called")
    
    style.use(plot_style)
    
    path="StaticPlot"

    if not os.path.exists(path):
        os.makedirs(path)

    pdf_file_name= f"{path}/num_num_var_plot" + datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d-%m-%y_%H%M") + ".pdf"   
    graph_pdf = PdfPages(pdf_file_name)
    logging.info(f"Creatin PDF File : {pdf_file_name}")
  
    try:
        numerical_var_list=df.select_dtypes(exclude=["object"])
        for column in numerical_var_list:

            work_figure = plt.figure(constrained_layout=False, figsize=plot_size(graphsize))
            grid = gridspec.GridSpec(ncols=2, nrows=2, figure=work_figure)
            
            try:
                logging.info(f"Ploting num_num_var_plot : ax1 for {column}")
                ax1 = work_figure.add_subplot(grid[0, :1])
                ax1.set_title(column.upper()+': Density Plot')
                sns.distplot(df[column],ax = ax1)
            except Exception as e:
                logging.exception(str(e))


            try:
                logging.info(f"Ploting num_num_var_plot : ax2 for {column}") 
                ax2 = work_figure.add_subplot(grid[1, :1])
                plt.hist(data = df,x=column)
                plt.title(column.upper()+' : Histogram',ax = ax2)
            except Exception as e:
                logging.exception(str(e)) 


            try:
                logging.info(f"Ploting num_num_var_plot : ax3 for {column}") 
                ax3 = work_figure.add_subplot(grid[0, 1])
                sns.boxplot(df[column], ax=ax3)
                plt.title(column.upper() + " : Box Plot")
            except Exception as e:
                logging.exception(str(e))


            try:
                logging.info(f"Ploting num_num_var_plot : ax4 for {column}") 
                ax4 = work_figure.add_subplot(grid[1, 1])
                sns.regplot(x=column, y=target_col, data=df,ax=ax4)
                plt.title(column.upper() + " Vs. "+target_col.upper()+" : Reg./Scatter Plot" )
                pearson_coef, p_value = stats.pearsonr(df[column], df[target_col])
                vals="Pearson_coef : "+ str(pearson_coef)
                ax4.text(0.5,0.7,vals,
                        horizontalalignment='left',
                        verticalalignment='center',
                        transform = ax4.transAxes,color='b', weight='bold',fontsize = 15)
            except Exception as e:
                logging.exception(str(e))

            work_figure.tight_layout() 
            # plt.show()
            logging.info(f"Saving num_num_var_plot in PDF for : {column}")
            graph_pdf.savefig(work_figure)

    except Exception as e:
        logging.exception(str(e))

    graph_pdf.close()
    return None


## ******Null Vs. Numerical Target variable
def null_num_var_plot(df,target_col,graphsize="big",plot_style="ggplot"):
    """
    Use : Create PDF Plot file for
    Null Vs. Numerical Target Variable
    Return : None

    Graphsize=A4,A3,mid,big default=big
    #print(plt.style.available)
    """
    logging.info("null_num_var_plot : Called")
    
    style.use(plot_style)
    
    path="StaticPlot"

    if not os.path.exists(path):
        os.makedirs(path)

    pdf_file_name= f"{path}/null_num_var_plot" + datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d-%m-%y_%H%M") + ".pdf"   
    graph_pdf = PdfPages(pdf_file_name)
    logging.info(f"Creatin PDF File : {pdf_file_name}")

    try:
        for column in df:
            df_temp=df.copy()
            df_temp[column]=np.where(df[column].isnull(),"Null","Not Null")
            grouped_data=df_temp.groupby(column)[target_col]
            
            if (df[column].isnull().sum()>=1):     
                work_figure = plt.figure(constrained_layout=False, figsize=plot_size(graphsize))
                grid = gridspec.GridSpec(ncols=2, nrows=2, figure=work_figure)

                try:
                    logging.info(f"Ploting null_num_var_plot : ax1 for {column}")
                    ax1 = work_figure.add_subplot(grid[0,0]) ## 1st Row, 1 Column
                    ax1.set_title(column.upper() + ' : Null Value MEDIAN Analysis')
                    grouped_data.median().plot.bar(ax = ax1)
                    for p in ax1.patches:
                        ax1.annotate('{:.0f}'.format(p.get_height()),(p.get_x()+0.2, p.get_height()+2))
                except Exception as e:
                    logging.exception(str(e))


                try:
                    logging.info(f"Ploting null_num_var_plot : ax2 for {column}")
                    ax2 = work_figure.add_subplot(grid[1,0]) ## 1st Row, 2 Column
                    ax2.set_title(column.upper() + ' : Null Value MEAN Analysis')
                    grouped_data.mean().plot.bar(ax = ax2) 
                    for p in ax2.patches:
                        ax2.annotate('{:.0f}'.format(p.get_height()),(p.get_x()+0.2, p.get_height()+2))
                except Exception as e:
                    logging.exception(str(e))

                try:
                    logging.info(f"Ploting null_num_var_plot : ax3 for {column}")
                    ax3 = work_figure.add_subplot(grid[0,1])
                    ax3.set_title(column.upper() + ' : Null Value Count Analysis')
                    grouped_data.count().plot.bar(ax = ax3) 
                    for p in ax3.patches:
                        ax3.annotate('{:.0f}'.format(p.get_height()),(p.get_x()+0.2, p.get_height()+2))
                except Exception as e:
                    logging.exception(str(e))

                try:
                    logging.info(f"Ploting null_num_var_plot : ax4 for {column}")
                    ax4 = work_figure.add_subplot(grid[1,1])
                    ax4.set_title(column.upper() + ' : Null Value Count Analysis')
                    Null_val_per=f"Null Value % : {np.round(df[column].isnull().mean()*100,2)}" 
                    ax4.text(0.5,0.5,Null_val_per,
                            horizontalalignment='left',
                            verticalalignment='center',
                            transform = ax4.transAxes,color='b', weight='bold',fontsize = 15)  
                except Exception as e:
                    logging.exception(str(e))

                work_figure.tight_layout(pad=10, w_pad=10, h_pad=10.0)
                #plt.show()
                logging.info(f"Saving Null_num_var_plot in PDF for : {column}")
                graph_pdf.savefig(work_figure)

    except Exception as e:
        logging.exception(str(e))

    graph_pdf.close()
    return None





##*****************************************************************************************  
## ************************* Function for Categorical Target Variavble ********************


## ******Categorical Vs. Categorical Target variable
def cat_cat_var_plot(df,target_col,graphsize="big",plot_style="ggplot"):
    """
    Use : Create PDF Plot file for
    Categorical Vs. Categorical Target Variable
    Return : None

    Graphsize=A4,A3,mid,big default=big
    #print(plt.style.available)
    """
    logging.info("cat_cat_var_plot : Called")
    
    style.use(plot_style)
    
    path="StaticPlot"

    if not os.path.exists(path):
        os.makedirs(path)

    pdf_file_name= f"{path}/cat_cat_var_plot" + datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d-%m-%y_%H%M") + ".pdf"   
    graph_pdf = PdfPages(pdf_file_name)
    logging.info(f"Creatin PDF File : {pdf_file_name}")
 
    
    try:
        categorical_var_list=df.select_dtypes(include=["object"])

        for column in categorical_var_list:    
            work_figure = plt.figure(constrained_layout=False, figsize=plot_size(graphsize))
            grid = gridspec.GridSpec(ncols=2, nrows=2, figure=work_figure)

            try:
                logging.info(f"Ploting cat_cat_var_plot : ax1 for {column}")
                ax1 = work_figure.add_subplot(grid[0,0]) ## 1st Row, 1 Column
                ax1.set_title(column.upper() + ' : Count Plot')
                sns.countplot(x=column,data = df,
                            order = df[column].value_counts().index,ax = ax1)
                plt.xticks(rotation=90)
                for p in ax1.patches:
                    ax1.annotate('{:.0f}'.format(p.get_height()),(p.get_x()+0.2, p.get_height()+2))
            except Exception as e:
                    logging.exception(str(e))

            try:
                logging.info(f"Ploting cat_cat_var_plot : ax2 for {column}")
                ax2 = work_figure.add_subplot(grid[1, 0]) ## 2 nd Row, 1 Column
                ax2.set_title(column.upper() + ' : Stack Column Plot ')
                sns.countplot(x=column,data = df,
                            order = df[column].value_counts().index,
                            hue=target_col,ax = ax2)
                for p in ax2.patches:
                    ax2.annotate('{:.0f}'.format(p.get_height()),(p.get_x()+0.2, p.get_height()+2))
                #df_plot = df.groupby([target_col,column]).size().reset_index().pivot(columns=target_col, index=column, values=0)
                #df_plot.plot(kind='bar', stacked=True,ax = ax2)
                plt.xticks(rotation=90)
            except Exception as e:
                logging.exception(str(e))


            try: 
                logging.info(f"Ploting cat_cat_var_plot : ax3 for {column}")       
                ax3 = work_figure.add_subplot(grid[:, 1]) ## Entire 2nd Column >>  [:, 1] This use complete Second Column
                df[column].value_counts().plot.pie(autopct = "%2.2f%%", ax=ax3)
                ax3.set_title(column.upper() + ' : Pie Plot')
            except Exception as e:
                logging.exception(str(e))

            work_figure.tight_layout()
            #plt.show()
            logging.info(f"Saving cat_cat_var_plot in PDF for : {column}")
            graph_pdf.savefig(work_figure)

    except Exception as e:
        logging.exception(str(e))

    graph_pdf.close()

    return None


## ******Numerical Vs. Categorical Target variable
def num_cat_var_plot(df,target_col,graphsize="big",plot_style="ggplot"):
    """
    Use : Create PDF Plot file for
    Numerical Vs. Categorical Target Variable
    Return : None

    Graphsize=A4,A3,mid,big default=big
    #print(plt.style.available)
    """
    logging.info("num_cat_var_plot : Called")
    
    style.use(plot_style)
    
    path="StaticPlot"

    if not os.path.exists(path):
        os.makedirs(path)

    pdf_file_name= f"{path}/num_cat_var_plot" + datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d-%m-%y_%H%M") + ".pdf"   
    graph_pdf = PdfPages(pdf_file_name)
    logging.info(f"Creatin PDF File : {pdf_file_name}")
 
    try:
        numerical_var_list=df.select_dtypes(exclude=["object"])
        for column in numerical_var_list:
            work_figure = plt.figure(constrained_layout=False, figsize=plot_size(graphsize))## Width , Height
            grid = gridspec.GridSpec(ncols=2, nrows=2, figure=work_figure)

            try:
                logging.info(f"Ploting num_cat_var_plot : ax1 for {column}")
                ax1 = work_figure.add_subplot(grid[0, :1])
                ax1.set_title(column.upper()+': Density Plot')
                sns.distplot(df[column],ax = ax1)
            except Exception as e:
                logging.exception(str(e))


            try:
                logging.info(f"Ploting num_cat_var_plot : ax2 for {column}")  
                ax2 = work_figure.add_subplot(grid[1, :1])
                plt.hist(data = df,x=column)
                plt.title(column.upper()+' : Histogram',ax = ax2)
            except Exception as e:
                logging.exception(str(e))

            try:
                logging.info(f"Ploting num_cat_var_plot : ax3 for {column}")
                ax3 = work_figure.add_subplot(grid[0, 1])
                sns.boxplot(df[column], ax=ax3)
                plt.title(column.upper() + " : Box Plot")
            except Exception as e:
                logging.exception(str(e))

            try:
                logging.info(f"Ploting num_cat_var_plot : ax4 for {column}")
                ax4 = work_figure.add_subplot(grid[1, 1])
                ax4.set_title(column.upper() + ' : Box Plot ')
                sns.boxplot(x=target_col, y=column, data = df,
                            order = df[target_col].value_counts().index,ax=ax4)
                plt.xticks(rotation=90)
            except Exception as e:
                logging.exception(str(e))

            work_figure.tight_layout() 
            #plt.show()
            logging.info(f"Saving num_cat_var_plot in PDF for : {column}")
            graph_pdf.savefig(work_figure)

    except Exception as e:
        logging.exception(str(e))

    graph_pdf.close()

    return None


## ******Null Vs. Categorical Target variable
def null_cat_var_plot(df,target_col,graphsize="big",plot_style="ggplot"):
    """
    Use : Create PDF Plot file for
    Null Vs. Categorical Target Variable
    Return : None

    Graphsize=A4,A3,mid,big default=big
    #print(plt.style.available)
    """
    logging.info("null_cat_var_plot : Called")
    
    style.use(plot_style)
    
    path="StaticPlot"

    if not os.path.exists(path):
        os.makedirs(path)

    pdf_file_name= f"{path}/null_cat_var_plot" + datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d-%m-%y_%H%M") + ".pdf"   
    graph_pdf = PdfPages(pdf_file_name)
    logging.info(f"Creatin PDF File : {pdf_file_name}")

    try:
        for column in df:
            df_temp=df.copy()
            df_temp[column]=np.where(df[column].isnull(),"Null","Not Null")
            grouped_data=df_temp.groupby(column)[target_col]
            
        if (df[column].isnull().sum()>=1):     
            work_figure = plt.figure(constrained_layout=False, figsize=plot_size(graphsize))
            grid = gridspec.GridSpec(ncols=2, nrows=2, figure=work_figure)

            try:
                logging.info(f"Ploting null_cat_var_plot : ax1 for {column}")
                ax1 = work_figure.add_subplot(grid[0,0]) ## 1st Row, 1 Column
                ax1.set_title(column.upper() + ' : Null Value COUNT Analysis')
                grouped_data.count().plot.bar(ax = ax1)
                for p in ax1.patches:
                    ax1.annotate('{:.0f}'.format(p.get_height()),(p.get_x()+0.2, p.get_height()+2))
            except Exception as e:
                logging.exception(str(e))

            try:
                logging.info(f"Ploting null_cat_var_plot : ax2 for {column}")
                ax2 = work_figure.add_subplot(grid[0,1])
                ax2.set_title(column.upper() + ' : Null Value Count Analysis')
                
                Null_val_per=f"Null Value % : {np.round(df[column].isnull().mean()*100,2)}" 

                ax2.text(0.5,0.5,Null_val_per,
                        horizontalalignment='left',
                        verticalalignment='center',
                        transform = ax2.transAxes,color='b', weight='bold',fontsize = 15)  
            except Exception as e:
                logging.exception(str(e))

            try:
                logging.info(f"Ploting null_cat_var_plot : ax3 for {column}")
                ax3 = work_figure.add_subplot(grid[1,0])
                ax3.set_title('Not Applicable')
            except Exception as e:
                logging.exception(str(e))
            
            try:
                logging.info(f"Ploting null_cat_var_plot : ax4 for {column}")
                ax4 = work_figure.add_subplot(grid[1,1])
                ax4.set_title('Not Applicable')
            except Exception as e:
                logging.exception(str(e))
            
            work_figure.tight_layout(pad=10, w_pad=10, h_pad=10.0)
            #plt.show()
            logging.info(f"Saving null_cat_var_plot in PDF for : {column}")
            graph_pdf.savefig(work_figure) #papertype=graphsize

    except Exception as e:
        logging.exception(str(e))

    graph_pdf.close()

    return None

##*************************************************************************
## ************************* Multivariate Analysis ************************
def mul_var_plot(df,target_col,graphsize="big",plot_style="ggplot"):
    """
    Use : Create PDF Plot file for
    mul var plot
    Return : None

    Graphsize=A4,A3,mid,big default=big
    #print(plt.style.available)
    """
    logging.info("mul_var_plot : Called")
    
    style.use(plot_style)
    
    path="StaticPlot"

    if not os.path.exists(path):
        os.makedirs(path)

    pdf_file_name= f"{path}/mul_var_plot" + datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d-%m-%y_%H%M") + ".pdf"   
    graph_pdf = PdfPages(pdf_file_name)
    logging.info(f"Creatin PDF File : {pdf_file_name}")

    try:
        logging.info(f"Ploting mul_var_plot-1")
        work_figure_1 = plt.figure(constrained_layout=False, figsize=plot_size(graphsize))
        corr = df.corr()
        # Generate a mask for the upper triangle
        mask = np.triu(np.ones_like(corr, dtype=np.bool))
        # Generate a custom diverging colormap
        cmap = sns.diverging_palette(220, 10, as_cmap=True)
        sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                    square=True, linewidths=.5, cbar_kws={"shrink": .5},annot=True,fmt='.2f', annot_kws={'size': 6}).set_title('Correlation Chart-1')
        work_figure_1.tight_layout()
        #plt.show()
        logging.info(f"Saving mul_var_plot-1 in PDF")
        graph_pdf.savefig(work_figure_1) 
    except Exception as e:
        logging.exception(str(e))

  
    try:
        logging.info(f"Ploting mul_var_plot-2")
        work_figure_2 = plt.figure(constrained_layout=False, figsize=plot_size(graphsize))
        corrSale=pd.DataFrame(corr[target_col])
        corrSale.reset_index(inplace=True)
        corrSale.sort_values(by=target_col,ascending=True,inplace=True)
        corrSale.dropna(inplace=True)
        corrSale.columns=["Feature","Value"]
        sns.barplot(y="Feature",x="Value",data=corrSale).set_title('Correlation Chart-2')
        plt.axvline(x=0)
        work_figure_2.tight_layout() 
        #plt.show()
        logging.info(f"Saving mul_var_plot-2 in PDF")
        graph_pdf.savefig(work_figure_2)
    except Exception as e:
        logging.exception(str(e))

    graph_pdf.close()

    return None