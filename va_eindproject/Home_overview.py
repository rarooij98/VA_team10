import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import time

# ---------------- SETTINGS -------------------
page_title = 'Eindproject VA'
# https://www.webfx.com/tools/emoji-cheat-sheet/
page_icon = ':oncoming_automobile:'
layout = 'centered'

st.set_page_config(
    page_title=page_title,
    page_icon=page_icon,
    layout=layout,
    initial_sidebar_state="expanded",
)

# ----------------- DATA ----------------------
# import data here

# ----------------- PAGES ---------------------
st.title(page_title + ' ' + page_icon)

st.write('''
         # Introductie 
         ...
''')