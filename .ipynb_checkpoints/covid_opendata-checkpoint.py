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

#SETTTING THE PAGE TITLE AND ICON

st.set_page_config(layout="wide", page_title= 'Covid Dashboards', page_icon="😷" )
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
    not_countries = ['OWID_EUN', 'OWID_INT']
    covid_w = covid_our [~covid_our['iso_code'].isin(not_countries)]
    country_shapes = json.load(open('world-countries.json'))
    return covid_our,covid_w, country_shapes
covid_our,covid_w, country_shapes = load_data()




#SIDEBAR
#IMAGE IN THE SIDEBAR
from PIL import Image
st.sidebar.image('images/covid_red.png', width=110)
#st.sidebar.title('''Covid-19 Dashboards''') 
st.sidebar.write (''' 📈 This app explore COVID-19 data at global level.''')

st.sidebar.header('''First Select the time period''') 
st.sidebar.write (''' If you want to analyse since Covid-19 starting leave in blank.''')

start_date = st.sidebar.date_input('SELECT START DATE', value =datetime(2020, 1, 1))
end_date = st.sidebar.date_input('SELECT END DATE')
st.sidebar.markdown ('---')
# SELECTORS SIDEBAR
normal = st.sidebar.checkbox("If you want the analysis relative to population")


st.sidebar.markdown ('---')
#footer
st.sidebar.write (''' 💡 This app use open Datasets from Our World Data. More details here''')
st.sidebar.write ('''💻 The code is available here.''')

st.sidebar.write ('''Instructions:''')
st.sidebar.write ('''1. ''')
st.sidebar.write ('''2. ''')
st.sidebar.write ('''3. ''')



st.markdown ('<h1 style= "font-family:Verdana; color:Black; font-size: 40px;">Covid Interactive Dashboards </h1>', unsafe_allow_html=True)
#st.text('this is app')
st.write (''' 
This app present interactive dashboards to explore COVID-19 data at global level. You can choose the region and countries, select the analysis, compare between the variables and countries, and select the time period.''')

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
    countries = st.multiselect("COUNTRY", country_continent['location'].unique())
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
if normal:   
    if variable == 'Cases':
        if interval == "Daily":
            fig = px.line( new_df, x = 'date', y = 'new_cases_per_million' , color = "location")
            fig.update_layout(title="<b>Daily new confirmed COVID-19 cases per million people<b>")
        
        elif interval == "7 days average":
            new_df['7_days_avg_pm'] = new_df['new_cases_per_million'].rolling(window=7).mean().round(2)  
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
else:
    
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
                                    linecolor='rgb(204, 204, 204)',
                                    linewidth=0.5,
                                    ticks='outside',
                                    tickmode="array",
                                    tickfont = dict(family = 'Arial', 
                                                    size = 12, 
                                                    color = 'rgb(82, 82, 82)'),
                                    showticklabels=True), 
                        yaxis = dict(title = 'Number of People', 
                                    showgrid=True,
                                     gridcolor = '#abd3df',
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



my_expander = st.beta_expander("ℹ️ Be safe from Coronovirus. Info", expanded=True)
with my_expander:
    st.markdown(""" Coronavirus disease (COVID-19) is an infectious disease caused by a newly discovered coronavirus.

📢 Most people infected with the COVID-19 virus will experience mild to moderate respiratory illness and recover without requiring special treatment.  Older people, and those with underlying medical problems like cardiovascular disease, diabetes, chronic respiratory disease, and cancer are more likely to develop serious illness.

📈 The best way to prevent and slow down transmission is to be well informed about the causes and how it spreads. 

😷 Protect yourself and others from infection by washing your hands or using an alcohol based rub frequently and not touching your face. 
The COVID-19 virus spreads primarily through droplets of saliva or discharge from the nose when an infected person coughs or sneezes, so it’s important that you also practice respiratory etiquette (for example, by coughing into a flexed elbow).
More info in: (https://www.who.int/health-topics/coronavirus#tab=tab_1)""")

                          
                          