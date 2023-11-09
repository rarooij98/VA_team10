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
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

df = load_data("./data/df.csv")
CO2 = load_data("./data/CO2.csv")
GDP = load_data("./data/GDP.csv")

# ----------------- PAGES ---------------------
st.title(page_title + ' ' + page_icon)

#* Boxplot
def boxplot(df):
    # Group the dataframe by Year and calculate the average CO2 emission
    df_avg_co2 = df.groupby('Year')['CO2 emission (Tons)'].mean().reset_index()
    # Create the boxplot using Plotly Express
    fig = px.box(df_avg_co2, y='CO2 emission (Tons)', title='Gemiddelde CO2 Emissie per jaar')
    # Add labels to the axes
    fig.update_layout(yaxis_title='Gemiddelde CO2 Emissie (Tons)')
    # Show the boxplot
    st.plotly_chart(fig, use_container_width=True)

#* Scatterplot
def scatterplot(df):
    # Filter the dataframe to include only data points with GDP <= 20T
    df_filtered = df[df['GDP'] <= 20000000000000]
    # Create a scatter plot of CO2 emissions vs GDP (filtered)
    fig = px.scatter(df_filtered, x='GDP', y='CO2 emission (Tons)',trendline="ols", title='CO2 Emissies vs GDP')
    # Add labels and trendline
    fig.update_layout(xaxis_title='GDP', yaxis_title='CO2 Emissie (Tons)')
    fig.update_traces(line=dict(color='red', width=2, dash='dash'))
    # Show the scatter plot
    st.plotly_chart(fig, use_container_width=True)
    
#* Histogram / Bar
def histogram_co2(df):  
    # Group the dataframe by Year and calculate the average CO2 emission
    df_avg_co2 = df.groupby('Year')['CO2 emission (Tons)'].mean().reset_index()
    fig = px.bar(df_avg_co2, x='Year', y='CO2 emission (Tons)', title='Gemiddelde CO2 Emissie per jaar')
    # Add a slider to select the year
    fig.update_layout(xaxis=dict(type='category'), xaxis_title='Jaar', yaxis_title='Gemiddelde CO2 Emissie (Tons)')
    fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)', marker_line_width=1.5)
    y_axis_range = [0, df_avg_co2['CO2 emission (Tons)'].max() + 10]
    fig.update_yaxes(range=y_axis_range)
    sliders = [dict(
        active=0,
        steps=[
            dict(
                label=str(year),
                method="update",
                args=[{"x": [df_avg_co2['Year']], "y": [df_avg_co2['CO2 emission (Tons)']*(df_avg_co2['Year'] == year)],
                       "text": [df_avg_co2['Year'] if year == y else '' for y in df_avg_co2['Year']]}],
            )
            for year in df_avg_co2['Year']
        ]
    )]
    fig.update_layout(
        sliders=sliders
    )
    # Display the figure in the Streamlit app
    st.plotly_chart(fig, use_container_width=True)
    
def bar_gdp(df):
    # Create the bar chart using Plotly Express to display average GDP per year
    df_avg_gdp = df.groupby('Year', as_index=False)['GDP'].mean()
    fig = px.bar(df_avg_gdp, x='Year', y='GDP', title='Gemiddelde GDP per jaar')
    st.plotly_chart(fig, use_container_width=True)

#* Call each plot in their own tab
# tab1, tab2, tab3 = st.tabs(["Boxplot", "Scatterplot", "Histogram"])
tab1, tab2 = st.tabs(["1D", "2D"])

with tab1:
   histogram_co2(df)
   bar_gdp(df)
   boxplot(df)
with tab2:
   scatterplot(df)

# Sources
# st.caption('Data: CO2 Emission by countries Year wise (1750-2022), https://www.kaggle.com/datasets/moazzimalibhatti/co2-emission-by-countries-year-wise-17502022')