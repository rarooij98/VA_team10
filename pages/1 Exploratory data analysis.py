import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# ---------------- SETTINGS -------------------
page_title = 'Exploratory data analysis'
page_icon = '📊' # https://html-css-js.com/html/character-codes/
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

#* Boxplot
def boxplot(df):
    # Group the dataframe by Year and calculate the average CO2 emission
    df_avg_co2 = df.groupby('Year')['CO2 emission (Tons)'].mean().reset_index()
    # Create the boxplot using Plotly Express
    fig = px.box(df_avg_co2, y='CO2 emission (Tons)', title='Average CO2 Emission by Year')
    # Add labels to the axes
    fig.update_layout(yaxis_title='Average CO2 Emission (Tons)')
    # Show the boxplot
    st.plotly_chart(fig, use_container_width=True)

#* Scatterplot
def scatterplot(df):
    # Filter the dataframe to include only data points with GDP <= 20T
    df_filtered = df[df['GDP'] <= 20000000000000]
    # Create a scatter plot of CO2 emissions vs GDP (filtered)
    fig = px.scatter(df_filtered, x='GDP', y='CO2 emission (Tons)',trendline="ols", title='CO2 Emissions vs GDP (Filtered)')
    # Add labels to the axes
    fig.update_layout(xaxis_title='GDP', yaxis_title='CO2 Emission (Tons)')
    # Add a trendline
    fig.update_traces(line=dict(color='red', width=2, dash='dash'))
    # Show the scatter plot
    st.plotly_chart(fig, use_container_width=True)

#* Call each plot in their own tab
# tab1, tab2, tab3 = st.tabs(["Boxplot", "Scatterplot", "Histogram"])
tab1, tab2 = st.tabs(["1D", "2D"])

with tab1:
   boxplot(df)
with tab2:
   scatterplot(df)

# Sources
# st.caption('Data: CO2 Emission by countries Year wise (1750-2022), https://www.kaggle.com/datasets/moazzimalibhatti/co2-emission-by-countries-year-wise-17502022')