import pandas as pd
import numpy as np

#libraries for matplotlib charts
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rcParams

#libraries for Plotly graphs
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots

import json
from geopy.geocoders import Nominatim  # convert address into latitude and longitude 
import requests # library to handle requests

#building the app
import streamlit as st #creating an app
from streamlit_folium import folium_static 
import folium #using folium on 


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

# Only show the dataframe with these columns
new_df = covid_w[covid_w['location'].isin(countries)]

# adding a chart 
fig = px.line( new_df, x = 'date', y = 'total_cases', color = "location", template="simple_white")

fig.update_layout(plot_bgcolor="white", 
                        xaxis = dict(
                                    title = 'Date', 
                                    showline=True,
                                    showgrid=False,
                                    linecolor='rgb(204, 204, 204)',
                                    linewidth=0.5,
                                    ticks='outside',
                                    tickfont = dict(
                                        family = 'Arial', 
                                        size = 14, 
                                        color = 'rgb(82, 82, 82)'),
                                    ), 
                        yaxis = dict(title = 'Number of People', 
                                    showgrid=True,
                                    zeroline=False,
                                    showline=False,
                                    linecolor='rgb(204, 204, 204)',
                                    linewidth=0.5,
                                    showticklabels=True), 
                        legend_title=dict(text='<b>Countries</b>',
                                     font=dict(
                                     size = 16)),
                 )
#margin=dict(t=10,l=10,b=10,r=10)

st.plotly_chart(fig, use_container_width=True)



