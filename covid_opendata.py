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

import altair as alt

#download the data
covid_our = pd.read_csv('https://github.com/owid/covid-19-data/blob/master/public/data/owid-covid-data.csv?raw=true')
covid_our

st.bar_chart(covid_our)
