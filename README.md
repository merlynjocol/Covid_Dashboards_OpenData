Table of Content
================
* [Covid Dashboards with OpenData](#Covid-Dashboards-with-OpenData)
  * [Description](#Description)
  * [Dataset](#Dataset)
  * [Installation Requirements](#Installation-Requirements)
  * [Software Heritage](#Software-Heritage)
  * [Licensing](#Licensing)
  * [Credits](#Credits)

# Covid Dashboards with OpenData

**Data Analysis Team:** [Adam Kozlowski](https://github.com/kozload), [Lisa Formentini](https://github.com/fmtlisa), [Merlyn Johanna Hurtado](https://github.com/merlynjocol)

# Description
This project is developed during the Course Open Data at the Master AIRE in the [Center for Research and Interdisciplinarity -CRI- ](https://cri-paris.org/en)

The main goal of this project is to built and deploy interactive dashboards using open data and data analysis

### Run the Dashboard

https://share.streamlit.io/merlynjocol/covid_dashboards_opendata/main/covid_opendata.py

1. Select the TIME PERIOD. The data is daily from 01-01-2020

2. Select the COUNTRY or COUNTRIES, the METRIC to analyse and the interval

3.  Select NORMALIZED data if you want to do analyses of the metrics relative by population in the country

# Dataset 
 The dataset  is from OurWorldData 
 
 https://github.com/owid/covid-19-data/blob/master/public/data/owid-covid-data.csv?raw=true
 

 ### Description of the variables:

- iso_code= ISO 3166-1 alpha-3 – three-letter country codes
- continent= Continent of the geographical location
- location=	Geographical location
- date=	Date of observation
- total_cases= Total confirmed cases of COVID-19 on a date in a country (cumulative)
- new_cases= New confirmed cases of COVID-19 on a date in a country 
- new_cases_permillion= New confirmed cases of COVID-19 per million habitants on a date in a country 
- new_cases_smoothed= New confirmed cases of COVID-19 (7-day smoothed)
- total_deaths= Total deaths attributed to COVID-19 on a date in a country (cumulative)
- new_deaths= New deaths attributed to COVID-19 in a country on a particular day 
- new_deaths_permillion= New deaths attributed to COVID-19 per million habitants in a country on a particular day
- new_deaths_smoothed= New deaths attributed to COVID-19 (7-day smoothed)
- people_fully_vaccinated= Total number of people who received all doses prescribed by the vaccination protocol

# Installation Requirements

To install the project dependencies run pip install -r requirements.txt
```
pip install -r requirements.txt
```

 #### requirements:
 
- pandas == 1.1.3
- numpy == 1.20.0
- plotly == 4.14.3
- streamlit == 0.81.1

# Software Heritage

[![SWH](https://archive.softwareheritage.org/badge/swh:1:dir:8c6d93d091c8e0fa0b8e2133183f6867cac42540/)](https://archive.softwareheritage.org/swh:1:dir:8c6d93d091c8e0fa0b8e2133183f6867cac42540)

# Licensing

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Credits

Many thanks to [Pierre Poulain](https://github.com/pierrepo), our project mentor
