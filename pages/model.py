import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st
import plotly.express as px

# ---------------- SETTINGS -------------------
page_title = 'Titel'
 #https://www.webfx.com/tools/emoji-cheat-sheet/
page_icon = '👋'
layout = 'centered'

st.set_page_config(
    page_title=page_title,
    page_icon=page_icon,
    layout=layout,
    initial_sidebar_state="expanded",
)

# ----------------- DATA ----------------------
CO2 = pd.read_csv("./data/CO2.csv")
GDP = pd.read_csv("./data/GDP.csv")
df = pd.read_csv("./data/df.csv")

# ----------------- PAGES ---------------------
st.title(page_title + ' ' + page_icon)

# page content ...
st.write(df)