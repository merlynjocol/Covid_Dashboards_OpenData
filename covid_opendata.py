import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import plotly.graph_objects as go
import json
#from geopy.geocoders import Nominatim  # convert address into latitude and longitude 
#import requests 
import streamlit as st



#Importing data
st.cache(persist=True)
def load_data():
    skipcols = ['total_cases_per_million',
       'total_deaths_per_million', 'reproduction_rate', 'icu_patients',
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

st.set_page_config(layout="wide")

# Header
st.title("COVID-19 Interactive Dashboards")
#st.text('this is app')
st.write (''' 
📈 This app present interactive dashboards to explore COVID-19 data at global level. You can choosee the region and countries, select the analysis, compare between the variables and countries, and select the time period.''')

#SIDEBAR

st.sidebar.write (''' 
📈 This app explore COVID-19 data at global level''') 


page_names = ["Chart", "Map"]
page = st.sidebar.radio ("Navigation", page_names, index=1)

# SELECTORS SIDEBAR


#footer
st.sidebar.markdown ('---')
st.sidebar.write (''' 💡 This app use open Datasets from Our World Data. More details here''')
st.sidebar.write ('''💻 The code is available here.''')



#SECOND CONTAINER 
#Titles
st.subheader ('''Select the country, variable, analysis and time period''')


#Select the variable 
col1, col2, col3, col4 = st.beta_columns([15, 15, 15, 15])

with col1: 
    region = st.multiselect("Select a Region", covid_w['continent'].unique())
with col2:   
    #select the country
    countries = st.multiselect("Tap or add a Country",covid_w['location'].unique())
    # Built the dataframe with the countries selected
    new_df = covid_w[covid_w['location'].isin(countries)]
with col3:
        variable = st.selectbox("Select the Variable",("Cases","Deaths","Cases per million", "Deaths per million", "Deaths per million (smoothed on a week)", "Cases per million (smoothed on a week)"))
with col4:
    interval  = st.selectbox("Select the analysis",("New daily","Weekly","7 days average", "Cumulative"))


# Building the charts

ca = px.line( new_df, x = 'date', y = 'new_cases', color = "location")
#MODELO 1-WHITE BACKGROUND
ca.update_layout(title="Daily Cases of Covid19",
                 xaxis = dict(title = 'Date'), 
                 yaxis = dict(title = 'Number of People'),
                 legend_title=dict(text='<b>Countries</b>'), 
                 width = 800, height= 500) 
                 #plot_bgcolor= "white")
ca.update_xaxes(rangeslider_visible=True)
                 
#Death Chart 
de = px.line( new_df, x = 'date', y = 'new_deaths', color = "location")

de.update_layout(title="Daily Deaths by Covid19", 
                 xaxis = dict(title = 'Date'), 
                 yaxis = dict(title = 'Number of People'),
                 legend_title=dict(text='<b>Countries</b>'),
                  )

#Cases chart per million
ca_pm = px.line( new_df, x = 'date', y = 'new_cases_per_million', color = "location")

ca_pm.update_layout(title="Daily Cases of Covid19 per million habitants",
                 xaxis = dict(title = 'Date'), 
                 yaxis = dict(title = 'Number of People (in million)'),
                 legend_title=dict(text='<b>Countries</b>'),
                 )

#Death Chart per million
de_pm = px.line( new_df, x = 'date', y = 'new_deaths_per_million', color = "location")

de_pm.update_layout(title="Daily Deaths by Covid19 per million", 
                 xaxis = dict(title = 'Date'), 
                 yaxis = dict(title = 'Number of People (in million)'),
                 legend_title=dict(text='<b>Countries</b>'),
                 )

#Cases chart per million smoothed on week
ca_pms = px.line( new_df, x = 'date', y = 'new_cases_smoothed_per_million', color = "location")

ca_pms.update_layout(title="Daily Cases of Covid19 per million habitants",
                 xaxis = dict(title = 'Date'), 
                 yaxis = dict(title = 'Number of People (in million)'),
                 legend_title=dict(text='<b>Countries</b>'),
                 )

#Death Chart per million smoothed on week
de_pms = px.line( new_df, x = 'date', y = 'new_deaths_smoothed_per_million', color = "location")

de_pms.update_layout(title="Daily Deaths by Covid19 per million", 
                 xaxis = dict(title = 'Date'), 
                 yaxis = dict(title = 'Number of People (in million)'),
                 legend_title=dict(text='<b>Countries</b>'),
                  )


col1, col2 = st.beta_columns([3, 1])
with col1:
    if variable =='Cases':
        st.plotly_chart(ca, use_container_width=True)   
    elif variable =='Deaths':
        st.plotly_chart(de, use_container_width=True) 
    elif variable =='Cases per million':
        st.plotly_chart(ca_pm, use_container_width=True)   
    elif variable =='Deaths per million':
        st.plotly_chart(de_pm, use_container_width=True) 
    elif variable =='Cases per million smoothed on a week':
        st.plotly_chart(ca_pms, use_container_width=True)   
    elif variable =='Deaths per million smoothed on a week':
        st.plotly_chart(de_pms, use_container_width=True)    

with col2:   
    st.title('''  ''')
    st.date_input('Select start date', datetime.date(2020, 1, 1))
    st.date_input('Select end date')
    normalization = st.checkbox("Relative to population")

    
my_expander = st.beta_expander("ℹ️ Covid Info", expanded=True)
with my_expander:
    st.markdown(""" Coronavirus disease (COVID-19) is an infectious disease caused by a newly discovered coronavirus.

📢 Most people infected with the COVID-19 virus will experience mild to moderate respiratory illness and recover without requiring special treatment.  Older people, and those with underlying medical problems like cardiovascular disease, diabetes, chronic respiratory disease, and cancer are more likely to develop serious illness.

📈 The best way to prevent and slow down transmission is to be well informed about the causes and how it spreads. 

😷 Protect yourself and others from infection by washing your hands or using an alcohol based rub frequently and not touching your face. 
The COVID-19 virus spreads primarily through droplets of saliva or discharge from the nose when an infected person coughs or sneezes, so it’s important that you also practice respiratory etiquette (for example, by coughing into a flexed elbow).
More info in: (https://www.who.int/health-topics/coronavirus#tab=tab_1)""")
