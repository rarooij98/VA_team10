import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import time

# ---------------- SETTINGS -------------------
page_title = 'CO2 uitstoot & GDP'
page_icon = '🌎' # https://www.webfx.com/tools/emoji-cheat-sheet/
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
         We onderzoeken de CO2 emissies van landen over de jaren heen, en vergelijken de emissies van een land met het GDP. 
         Stoten landen met een hoger GDP meer uit, is deze verhouding over de jaren heen veranderd? We gebruiken een lineair 
         regressie model om de uitstoot voor komende jaren te voorspellen.
''')

# Show DataFrame with emission and GDP for each country per year
st.write('#### DataFrame')
st.write(df)