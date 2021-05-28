import streamlit as st
import pandas as pd # library for data analysis
from streamlit_folium import folium_static
import folium
import json
import requests
import numpy as np

from geopy.geocoders import Nominatim 
# convert an address into latitude and longitude values
import requests # library to handle requests
import streamlit as st #creating an app
from streamlit_folium import folium_static 
#using folium on 


#Importing the data

st.cache(persist=True)
def load_data():
    skipcols = ['total_cases_per_million',
       'new_cases_per_million', 'new_cases_smoothed_per_million',
       'total_deaths_per_million', 'new_deaths_per_million',
       'new_deaths_smoothed_per_million', 'reproduction_rate', 'icu_patients',
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
    return covid_our,covid_w
covid_our,covid_w= load_data()

st.title("COVID-19 Interactive Dashboards")
st.text('this is app')
st.write (''' This project presents interactive dashboards to explore covid-19 data at global level. You can choosee the countries and continents, compare between the number of cases, deaths and vaccination in a time period ''')


 #Select the variable 
 variable = st.multiselect("Select the Variable",("Cases","Deaths"))
 
 #select the country
 countries = st.multiselect("Select a Country or Countries",covid_w['location'].unique())
 # Only show dataframe with these columns
 new_df = covid_w[covid_w['location'].isin(countries)]


