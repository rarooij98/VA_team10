import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import time

# ---------------- SETTINGS -------------------
page_title = 'CO2 uitstoot & GDP'
page_icon = '🌎' # https://html-css-js.com/html/character-codes/
layout = 'centered'

st.set_page_config(
    page_title=page_title,
    page_icon=page_icon,
    layout=layout,
    initial_sidebar_state="expanded",
)

# ----------------- DATA ----------------------
df = pd.read_csv("./data/df.csv")

# ----------------- PAGES ---------------------
st.title(page_title + ' ' + page_icon)

st.write('''
         #### Introductie 
         In deze Streamlit app onderzoeken we de CO2 emissies van landen over de jaren heen, en vergelijken de emissies van een land met het GDP. 
         Welke landen stoten het meeste CO2 uit, hebben zij een hoger GDP? We gebruiken een lineair 
         regressie model om de uitstoot voor komende jaren te voorspellen aan de hand van de GDP en Population van landen.
''')

# Show DataFrame with emission and GDP for each country per year
st.write('#### DataFrame')

df = df[['Country', 'Code', 'Year', 'GDP', 'CO2 emission (Tons)', 'Area', '% of World', 'Density(km2)']]
st.write(df)