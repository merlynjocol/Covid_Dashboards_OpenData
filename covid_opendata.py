import pandas as pd
import numpy as np
import datetime
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import json
#from geopy.geocoders import Nominatim  # convert address into latitude and longitude 
#import requests 
import streamlit as st



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
    not_countries = ['OWID_EUN', 'OWID_INT']
    covid_w = covid_our [~covid_our['iso_code'].isin(not_countries)]
    country_shapes = json.load(open('world-countries.json'))
    return covid_our,covid_w, country_shapes
covid_our,covid_w, country_shapes = load_data()

#st.set_page_config(layout="wide")
padding = 3
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)


#SIDEBAR
#IMAGE IN THE SIDEBAR
from PIL import Image
col1, col2 = st.beta_columns([1, 1])
with col1: 
    st.sidebar.image('images/covid_red.png', width=110)
with col2: 
    st.sidebar.title('''Covid-19 Dashboards''') 
    
st.sidebar.write (''' 📈 This app explore COVID-19 data at global level''') 


page_names = ["Chart", "Map"]
page = st.sidebar.radio ("Navigation", page_names, index=1)

# SELECTORS SIDEBAR

#footer
st.sidebar.markdown ('---')
st.sidebar.write (''' 💡 This app use open Datasets from Our World Data. More details here''')
st.sidebar.write ('''💻 The code is available here.''')


# HEADER MAIN PAGE 
st.title("COVID-19 Interactive Dashboards")
#st.text('this is app')
st.write (''' 
This app present interactive dashboards to explore COVID-19 data at global level. You can choosee the region and countries, select the analysis, compare between the variables and countries, and select the time period.''')

#SECOND CONTAINER 
#Titles
st.subheader ('''📈 Select the country, metric, interval and time period for the analysis''')


# SELECT BOXES IN FRAMEWORK HORIZONTAL (Select a variable)
col1, col2, col3, col4 = st.beta_columns([1, 1, 1, 1])

with col1: 
    continent = st.selectbox("CONTINENT", covid_w['continent'].dropna().unique())
    country_continent = covid_w[covid_w['continent'] == continent ].groupby('location').count().reset_index()
with col2:   
    #select the country
    countries = st.multiselect("COUNTRY",country_continent['location'].unique())
    # Built the dataframe with the countries selected
with col3:
    variable = st.selectbox("METRIC",("Cases","Deaths"))                         
with col4:
    interval  = st.selectbox("INTERVAL",("Daily","Weekly","7 days average", "Cumulative", 
                                                    'Daily per million people',
                                                    "Cumulative per million people" ))
#STATE AN ERROR
if not countries:
    st.error(" ⚠️ Please select at least one country.")
    
    
# DF FOR VISUALISATIONS

covid_w['date'] = pd.to_datetime(covid_w['date']).dt.date # date format

new_df = covid_w[covid_w['location'].isin(countries)] # df for charts

                            
# BUILDING INTERACTIVES VISUALISATIONS                        
                            
                            
if variable == 'Cases':
    if interval == "Daily":
        fig = px.line( new_df, x = 'date', y = 'new_cases' , color = "location")
        fig.update_layout(title="Daily new confirmed COVID-19 cases")
    
     # NEED TO BUILT WEEKLY
    elif interval == "7 days average":
        new_df['7_days_avg'] = new_df['new_cases'].rolling(window=7).mean().round(2)  
        fig = px.line( new_df, x = 'date', y = '7_days_avg' , color = "location")
        fig.update_layout(title="Daily new confirmed COVID-19 cases shown is the rolling 7-day average", )     

    elif interval == "Cumulative":
        fig = px.line( new_df, x = 'date', y = 'total_cases' , color = "location")
        fig.update_layout(title="Cumulative confirmed COVID-19 cases")
                          
    elif interval == "Daily per million people":
        fig = px.line( new_df, x = 'date', y = 'new_cases_per_million' , color = "location")
        fig.update_layout(title="Daily new confirmed COVID-19 cases per million people")

    elif interval == "Cumulative per million people" :
        fig = px.line( new_df, x = 'date', y = 'total_cases_per_million' , color = "location")
        fig.update_layout(title="Cumulative confirmed COVID-19 cases per million people")                            
                            
elif variable =='Deaths':           
                       
    if interval == "Daily":
        fig = px.line( new_df, x = 'date', y = 'new_deaths' , color = "location")
        fig.update_layout(title="Daily new confirmed COVID-19 deaths")
    
     # NEED TO BUILT WEEKLY
    elif interval == "7 days average":
        new_df['7_days_avg'] = new_df['new_deaths'].rolling(window=7).mean().round(2)  
        fig = px.line( new_df, x = 'date', y = '7_days_avg' , color = "location")
        fig.update_layout(title="Daily new confirmed COVID-19 deaths shown is the rolling 7-day average", )     

    elif interval == "Cumulative":
        fig = px.line( new_df, x = 'date', y = 'total_deaths' , color = "location")
        fig.update_layout(title="Cumulative confirmed COVID-19 deaths")
                          
    elif interval == "Daily per million people":
        fig = px.line( new_df, x = 'date', y = 'new_deaths_per_million' , color = "location")
        fig.update_layout(title="Daily new confirmed COVID-19 deaths per million people")

    elif interval == "Cumulative per million people" :
        fig = px.line( new_df, x = 'date', y = 'total_deaths_per_million' , color = "location")
        fig.update_layout(title="Cumulative confirmed COVID-19 deaths per million people")                            


fig.update_layout( 
                 xaxis = dict(title = 'Date'), 
                 yaxis = dict(title = 'Number of People'),
                 legend_title=dict(text='<b>Countries</b>'),
                 width = 800, height= 500) 
    #fig.update_xaxes(rangeslider_visible=True)


col1, col2 = st.beta_columns([3, 1])
with col1:
    
    st.plotly_chart(fig, use_container_width=True)    
                          
                          
with col2:   
    st.title('''  ''')
    normalization = st.checkbox("Relative to population")
    start_date = st.date_input('Select start date', value =datetime(2020, 1, 1))
    end_date = st.date_input('Select end date', value = covid_w.date.max())

time_period =  covid_w.loc[(covid_w['date'] >= start_date) & (covid_w['date'] <= end_date),:] #time period  



my_expander = st.beta_expander("ℹ️ Covid Info", expanded=True)
with my_expander:
    st.markdown(""" Coronavirus disease (COVID-19) is an infectious disease caused by a newly discovered coronavirus.

📢 Most people infected with the COVID-19 virus will experience mild to moderate respiratory illness and recover without requiring special treatment.  Older people, and those with underlying medical problems like cardiovascular disease, diabetes, chronic respiratory disease, and cancer are more likely to develop serious illness.

📈 The best way to prevent and slow down transmission is to be well informed about the causes and how it spreads. 

😷 Protect yourself and others from infection by washing your hands or using an alcohol based rub frequently and not touching your face. 
The COVID-19 virus spreads primarily through droplets of saliva or discharge from the nose when an infected person coughs or sneezes, so it’s important that you also practice respiratory etiquette (for example, by coughing into a flexed elbow).
More info in: (https://www.who.int/health-topics/coronavirus#tab=tab_1)""")

                          
                          