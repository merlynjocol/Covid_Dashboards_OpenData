import pandas as pd
import numpy as np
import datetime
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import warnings
warnings.filterwarnings("ignore")

showWarningOnDirectExecution = false

#SETTTING THE PAGE TITLE AND ICON
st.set_page_config(layout="wide", page_title= 'Covid Dashboards', page_icon="📈" )

padding = 3
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)



#Importing data
st.cache(persist=True)
def load_data():
    skipcols = [
       'reproduction_rate', 'icu_patients',
       'icu_patients_per_million', 'hosp_patients',
       'hosp_patients_per_million', 'weekly_icu_admissions',
       'weekly_icu_admissions_per_million', 'weekly_hosp_admissions',
       'weekly_hosp_admissions_per_million', 'new_tests', 'total_tests',
       'total_tests_per_thousand', 'new_tests_per_thousand',
       'new_tests_smoothed', 'new_tests_smoothed_per_thousand',
       'positive_rate', 'tests_per_case', 'tests_units', 
       'new_vaccinations_smoothed', 'total_vaccinations_per_hundred',
       'people_vaccinated_per_hundred', 'people_fully_vaccinated_per_hundred',
       'new_vaccinations_smoothed_per_million', 'stringency_index',
       'population', 'population_density', 'median_age', 'aged_65_older',
       'aged_70_older']

    covid_our = pd.read_csv('https://github.com/owid/covid-19-data/blob/master/public/data/owid-covid-data.csv?raw=true', usecols=lambda x: x not in skipcols, index_col=0).reset_index()
    #dropping the rows with values that are not countries 
    not_countries = ['OWID_EUN', 
                     'OWID_INT', 
                     'OWID_AFR', 
                     'OWID_ASI',
                     'OWID_EUN',
                     'OWID_INT', 
                     'OWID_KOS', 
                     'OWID_NAM', 
                     'OWID_CYN', 
                     'OWID_OCE', 
                     'OWID_WRL']
    covid_w = covid_our [~covid_our['iso_code'].isin(not_countries)]
    return covid_our,covid_w
covid_our,covid_w = load_data()



#SIDEBAR
#IMAGE IN THE SIDEBAR
from PIL import Image
st.sidebar.image('images/covid_red.png', width=110)
#st.sidebar.title('''Covid-19 Dashboards''') 
st.sidebar.write (''' 📈 This app explore COVID-19 data Worldwide.''')
st.sidebar.header('''TIME PERIOD''') 
st.sidebar.write (''' Select the time period. If you want the analysis since Covid-19 started, leave in blank.''')
# SELECTORS SIDEBAR
start_date = st.sidebar.date_input('SELECT START DATE', datetime(2020, 1, 1))
end_date = st.sidebar.date_input('SELECT END DATE')
#SIDEBAR INFORMATION
st.sidebar.markdown ('---')
st.sidebar.header('''Information''') 
st.sidebar.write("💡 This app use open Datasets from Our World Data [link](https://github.com/owid/covid-19-data/blob/master/public/data/owid-covid-data.csv?raw=true)")
st.sidebar.write("💻 The code is available here: [link](https://github.com/merlynjocol/Covid_Dashboards_OpenData)")
#SIDEBAR INSTRUCTIONS
st.sidebar.markdown ('---')
st.sidebar.header('''Instructions''') 
st.sidebar.write ('''1. Select the TIME PERIOD. The data is daily from 01-01-2020''')
st.sidebar.write ('''2. Select the COUNTRY or COUNTRIES, the METRIC to analyse and the interval''')
st.sidebar.write ('''3. Select NORMALIZED data if you want to do analyses of the metrics relative by population in the country''')



st.markdown ('<h1 style= "font-family:Verdana; color:Black; font-size: 40px;">Covid Interactive Dashboards </h1>', unsafe_allow_html=True)
#st.text('this is app')
st.write (''' 
This app present interactive dashboards to explore COVID-19 data, to compare countries and variables at worldwide. Select the country or countries and the variable to analyze. If you want the analysis in a specific period of time, please choose the time period you need, it is located in the left-side of the WebApp. ''')

#SECOND CONTAINER 
#Titles
st.subheader ('''📈 SELECT. Choose the Country, Metric, Interval and Non/Normalized Data''')


# SELECT BOXES IN FRAMEWORK HORIZONTAL (Select a variable)
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

#with col1: 
    #continent = st.selectbox("CONTINENT", covid_w['continent'].dropna().unique())
    #country_continent = covid_w[covid_w['continent'] == continent ].groupby('location').count().reset_index()
with col1:   
    #select the country
    countries = st.multiselect("COUNTRY or COUNTRIES", covid_w['location'].unique())
    # Built the dataframe with the countries selected
with col2:
    variable = st.selectbox("METRIC",("Cases","Deaths"))                         
with col3:
    interval  = st.selectbox("INTERVAL",("Daily","7 days average", "Cumulative" ))
#STATE AN ERROR
if not countries:
    st.error(" ⚠️ Please select at least one country.")
with col4: 
    normal = st.selectbox("Analysis Relative to Population", ("Non-Normalized","Normalized"))


# DF FOR VISUALISATIONS
covid_w['date'] = pd.to_datetime(covid_w['date']).dt.date # date format
date_interval = covid_w.loc[(covid_w['date'] >= start_date) & (covid_w['date'] <= end_date),:]
new_df = date_interval[date_interval['location'].isin(countries)] # df for charts
new_df['7_days_avg_pm'] = new_df['new_cases_per_million'].rolling(window=7).mean().round(2)  


# BUILDING INTERACTIVES VISUALISATIONS                        
if normal ==  "Normalized":   
    if variable == 'Cases':
        if interval == "Daily":
            fig = px.line( new_df, x = 'date', y =  'new_cases_per_million' , color = "location")
            fig.update_layout(title="<b>Daily new confirmed COVID-19 cases per million people<b>")
        
        elif interval == "7 days average":
            fig = px.line( new_df, x = 'date', y = '7_days_avg_pm' , color = "location")
            fig.update_layout(title="<b>Daily new confirmed COVID-19 cases per million. 7-day average<b>", )
            
        
        elif interval == "Cumulative per million people" :
            fig = px.line( new_df, x = 'date', y = 'total_cases_per_million' , color = "location")
            fig.update_layout(title="<b>Cumulative confirmed COVID-19 cases per million people<b>")                            
                            
    elif variable =='Deaths':  
        if interval == "Daily per million people":
            fig = px.line( new_df, x = 'date', y = 'new_deaths_per_million' , color = "location")
            fig.update_layout(title="<b>Daily new confirmed COVID-19 deaths per million people<b>")
        
        elif interval == "7 days average":
            new_df['7_days_avg_pm'] = new_df['new_deaths_per_million'].rolling(window=7).mean().round(2)  
            fig = px.line( new_df, x = 'date', y = '7_days_avg_pm' , color = "location")
            fig.update_layout(title="<b>Daily new confirmed COVID-19 deaths shown is the rolling 7-day average<b>", )  
        
        elif interval == "Cumulative per million people" :
            fig = px.line( new_df, x = 'date', y = 'total_deaths_per_million' , color = "location")
            fig.update_layout(title="<b>Cumulative confirmed COVID-19 deaths per million people</b>") 

if normal==  "Non-Normalized":
    
    if variable == 'Cases':
        
        if interval == "Daily":
            fig = px.line( new_df, x = 'date', y = 'new_cases' , color = "location")
            fig.update_layout(title="<b>Daily new confirmed COVID-19 cases<b>")
        
        elif interval == "7 days average":
            new_df['7_days_avg'] = new_df['new_cases'].rolling(window=7).mean().round(2)  
            fig = px.line( new_df, x = 'date', y = '7_days_avg' , color = "location")
            fig.update_layout(title="<b>Daily new confirmed COVID-19 cases shown is the rolling 7-day average<b>", )     

        elif interval == "Cumulative":
            fig = px.line( new_df, x = 'date', y = 'total_cases' , color = "location")
            fig.update_layout(title="<b>Cumulative confirmed COVID-19 cases<b>")
                   
                            
    elif variable =='Deaths':           
                       
        if interval == "Daily":
            fig = px.line( new_df, x = 'date', y = 'new_deaths' , color = "location")
            fig.update_layout(title="<b>Daily new confirmed COVID-19 deaths<b>")
    
     
        elif interval == "7 days average":
            new_df['7_days_avg_d'] = new_df['new_deaths'].rolling(window=7).mean().round(2)  
            fig = px.line( new_df, x = 'date', y = '7_days_avg_d' , color = "location")
            fig.update_layout(title="<b>Daily new confirmed COVID-19 deaths shown is the rolling 7-day average<b>", )     

    
        elif interval == "Cumulative":
            fig = px.line( new_df, x = 'date', y = 'total_deaths' , color = "location")
            fig.update_layout(title="<b>Cumulative confirmed COVID-19 deaths<b>")
    
                
     

    
fig.update_layout(plot_bgcolor="white",
                       hovermode="x unified",                      
                       title=dict(font=dict(
                                     size = 22)),
                        xaxis = dict(title = 'Date', 
                                    showline=True,
                                    showgrid=True,
                                    linecolor='rgb(252, 252, 252)',
                                    linewidth=0.5,
                                    ticks='outside',
                                    tickmode="array",
                                    visible= True,
                                    tickfont = dict(family = 'Arial', 
                                                    size = 12, 
                                                    color = 'rgb(82, 82, 82)'),
                                    showticklabels=True), 
                        yaxis = dict(title = 'Number of People', 
                                    showgrid=True,
                                    gridcolor = 'rgb(204, 204, 204)',
                                    zeroline=False,
                                    showline=True,
                                    linecolor='rgb(204, 204, 204)',
                                    linewidth=0.5,
                                    tickmode="array",
                                    visible= True,
                                    ticks='outside',
                                    showticklabels=True), 
                        legend_title=dict(text='<b>Countries</b>',
                                     font=dict(
                                     size = 16)),
                         width = 700, height= 500)


   
st.plotly_chart(fig, use_container_width=True)    
                          
                          
time_period =  covid_w.loc[(covid_w['date'] >= start_date) & (covid_w['date'] <= end_date),:] #time period  



my_expander = st.beta_expander("ℹ️ COVID INFO. Be safe from Coronovirus 🥰", expanded=True)
with my_expander:
    st.markdown(""" Coronavirus disease (COVID-19) is an infectious disease caused by a newly discovered coronavirus.

📢 Most people infected with the COVID-19 virus will experience mild to moderate respiratory illness and recover without requiring special treatment.  Older people, and those with underlying medical problems like cardiovascular disease, diabetes, chronic respiratory disease, and cancer are more likely to develop serious illness.

📈 The best way to prevent and slow down transmission is to be well informed about the causes and how it spreads. 

😷 Protect yourself and others from infection by washing your hands or using an alcohol based rub frequently and not touching your face. 
The COVID-19 virus spreads primarily through droplets of saliva or discharge from the nose when an infected person coughs or sneezes, so it’s important that you also practice respiratory etiquette (for example, by coughing into a flexed elbow).
More info in: (https://www.who.int/health-topics/coronavirus#tab=tab_1)""")

                          
                          
