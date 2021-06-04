import pandas as pd
import numpy as np

#libraries for matplotlib charts
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rcParams

#libraries for Plotly graphs
import plotly.express as px
import plotly.figure_factory as ff
from plotly.subplots import make_subplots

#create templates
import plotly.graph_objects as go
import plotly.io as pio


import json
from geopy.geocoders import Nominatim  # convert address into latitude and longitude 
import requests # library to handle requests

#building the app
import streamlit as st #creating an app
from streamlit_folium import folium_static 
import folium #using folium on 



#Importing the data

#Importing the data


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
    contry_shapes = pd.read_json('https://github.com/python-visualization/folium/blob/master/examples/data/world-countries.json')
    #country_shapes = json.load(open('world-countries.json'))
    return covid_our,covid_w, country_shapes
covid_our,covid_w, country_shapes = load_data()



#FIRST CONTAINER 

st.title("COVID-19 Interactive Dashboards")
#st.text('this is app')
st.write (''' This project presents interactive dashboards to explore covid-19 data at global level. You can choosee the countries and continents, compare between the number of cases, deaths and vaccination in a time period ''')


#SECOND CONTAINER 
#Titles
st.header("1. Confirmed Cases and Deaths by Country")
st.write ('''Select the variable to analyse and the countrye''')

#Select the variable 
variable = st.selectbox("Select the Variable",("Cases","Deaths","Cases per million", "Deaths per million", "Deaths per million (smoothed on a week)", "Cases per million (smoothed on a week)"))
#select the country
countries = st.multiselect("Select a Country or Multiple countries",covid_w['location'].unique())

# Built the dataframe with the countries selected
new_df = covid_w[covid_w['location'].isin(countries)]

# Building the charts

#building my own template 
template_covid = dict(layout=go.Layout(title_font=dict(family="Helvetica", size=24), 
                                 plot_bgcolor="white", 
                                  xaxis = dict(
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
                                  yaxis = dict( 
                                    showgrid=True,
                                    zeroline=False,
                                    showline=False,
                                    linecolor='rgb(204, 204, 204)',
                                    linewidth=0.5,
                                    showticklabels=True),
                                  legend_title=dict(text='<b>Countries</b>',
                                     font=dict(
                                     size = 16)),
                 ))



# Build my own second template 
monochrome_colors = ['#251616', '#760000', '#C63F3F', '#E28073', '#F1D3CF']
primary_colors = ['#C63F3F', '#F4B436', '#83BFCC', '#455574', '#E2DDDB']

theme_covid2 = go.layout.Template(
            layout=go.Layout(
            title = {'font':{'size':18, 'family':"Helvetica", 
                             'color':monochrome_colors[0]}, 
                             'pad':{'t':100, 'r':0, 'b':0, 'l':0}},
            plot_bgcolor="#F4B436",
            font = {'size':18, 'family':'Helvetica', 'color':'#717171'},
            xaxis = {'ticks': "outside",
                'tickfont': {'size': 14, 'family':"Helvetica"},
                'showticksuffix': 'all',
                'showtickprefix': 'last',
                'showline': False,
                'showgrid' :False,
                'title':{'font':{'size':18, 'family':'Helvetica'}, 'standoff':20},
                'automargin': True,
                },
            yaxis = {'ticks': "outside",
                'tickfont': {'size': 14, 'family':"Helvetica"},
                'showticksuffix': 'all',
                'showtickprefix': 'last',
                'title':{'font':{'size':18, 'family':'Helvetica'}, 'standoff':20},
                'showline': True,
                'automargin': True,
                },
            legend = {'bgcolor':'rgba(0,0,0,0)', 
                'title':{'font':{'size':18, 'family':"Helvetica", 'color':monochrome_colors[0]}}, 
                'font':{'size':14, 'family':"Helvetica"}, 
                'yanchor':'bottom'
                },
                                                 
            colorscale = {'diverging':monochrome_colors,
                     
                     },
            coloraxis = {'autocolorscale':True, 
                'cauto':True, 
                'colorbar':{'tickfont':{'size':14,'family':'Helvetica'}, 
                            'title':{'font':{'size':18, 'family':'Helvetica'}}},
                },
            scene = {'xaxis': {'backgroundcolor': 'white',
                        'gridcolor': 'rgb(232,232,232)',
                        'gridwidth': 2,
                        'linecolor': 'rgb(36,36,36)',
                        'showbackground': True,
                        'showgrid': False,
                        'showline': True,
                        'ticks': 'outside',
                        'zeroline': False,
                        'zerolinecolor': 'rgb(36,36,36)',
                            }
                } 
        )
)
                 



#Cases chart
ca = px.line( new_df, x = 'date', y = 'new_cases', color = "location")

ca.update_layout(title="Daily Cases of Covid19",
                 xaxis = dict(title = 'Date'), 
                 yaxis = dict(title = 'Number of People'),
                 legend_title=dict(text='<b>Countries</b>'),
                 template=theme_covid2)
                 
#Death Chart 
de = px.line( new_df, x = 'date', y = 'new_deaths', color = "location")

de.update_layout(title="Daily Deaths by Covid19", 
                 xaxis = dict(title = 'Date'), 
                 yaxis = dict(title = 'Number of People'),
                 legend_title=dict(text='<b>Countries</b>'),
                 template=theme_covid2 )

#Cases chart per million
ca_pm = px.line( new_df, x = 'date', y = 'new_cases_per_million', color = "location")

ca_pm.update_layout(title="Daily Cases of Covid19 per million habitants",
                 xaxis = dict(title = 'Date'), 
                 yaxis = dict(title = 'Number of People (in million)'),
                 legend_title=dict(text='<b>Countries</b>'),
                 template=theme_covid2)

#Death Chart per million
de_pm = px.line( new_df, x = 'date', y = 'new_deaths_per_million', color = "location")

de_pm.update_layout(title="Daily Deaths by Covid19 per million", 
                 xaxis = dict(title = 'Date'), 
                 yaxis = dict(title = 'Number of People (in million)'),
                 legend_title=dict(text='<b>Countries</b>'),
                 template=theme_covid2 )

#Cases chart per million smoothed on week
ca_pm = px.line( new_df, x = 'date', y = 'new_cases_smoothed_per_million', color = "location")

ca_pm.update_layout(title="Daily Cases of Covid19 per million habitants",
                 xaxis = dict(title = 'Date'), 
                 yaxis = dict(title = 'Number of People (in million)'),
                 legend_title=dict(text='<b>Countries</b>'),
                 template=theme_covid2)

#Death Chart per million smoothed on week
de_pm = px.line( new_df, x = 'date', y = 'new_deaths_smoothed_per_million', color = "location")

de_pm.update_layout(title="Daily Deaths by Covid19 per million", 
                 xaxis = dict(title = 'Date'), 
                 yaxis = dict(title = 'Number of People (in million)'),
                 legend_title=dict(text='<b>Countries</b>'),
                 template=theme_covid2 )


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
