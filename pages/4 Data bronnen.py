import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns
import plotly.express as px
from statsmodels.formula.api import ols

# ---------------- SETTINGS -------------------
page_title = 'Data bronnen'
page_icon = '📑' # https://www.webfx.com/tools/emoji-cheat-sheet/
layout = 'centered'

st.set_page_config(
    page_title=page_title,
    page_icon=page_icon,
    layout=layout,
    initial_sidebar_state="expanded",
)

# ----------------- DATA ----------------------
# CO2 = pd.read_csv("./data/CO2.csv")
# GDP = pd.read_csv("./data/GDP.csv")
# df = pd.read_csv("./data/df.csv")
# df_mv = pd.read_csv("./data/df_mv.csv")
# total_data = pd.read_csv("./data/total_data.csv")

# ----------------- PAGES ---------------------
st.title(page_title + ' ' + page_icon)

st.write('* CO2 Emission by countries Year wise (1750-2022), https://www.kaggle.com/datasets/moazzimalibhatti/co2-emission-by-countries-year-wise-17502022')
st.write('* World GDP (GDP, GDP per capita, and annual growths), https://www.kaggle.com/datasets/zgrcemta/world-gdpgdp-gdp-per-capita-and-annual-growths?select=gdp.csv')
st.write('* World Population Data 1960-2020, https://www.kaggle.com/datasets/utkarshx27/world-population-data-1960-2020')
st.write('* Country Polygons as GeoJSON, https://datahub.io/core/geo-countries')