import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st
import plotly.express as px
import geopandas as gpd
import folium
from streamlit_folium import folium_static

# ---------------- SETTINGS -------------------
page_title = 'Geospatial data'
page_icon = '🌏' # https://html-css-js.com/html/character-codes/
layout = 'centered'

st.set_page_config(
    page_title=page_title,
    page_icon=page_icon,
    layout=layout,
    initial_sidebar_state="expanded",
)

# ----------------- DATA ----------------------
df = pd.read_csv("./data/df.csv")
gdf = gpd.read_file('./data/countries.geojson')

# ----------------- PAGES ---------------------
st.title(page_title + ' ' + page_icon)

#* Prepare DataFrame
# Rename 'United States of America' to 'United States'
df['Country'] = df['Country'].replace({'United States' : 'United States of America'})

gdf = gdf.rename(columns={'ADMIN' : 'Country'})

df_2 = df.loc[df['GDP'] > 0]
df_2 = df_2[df_2['Population(2022)'] > 0]
df_2 = df_2[df_2['Area'] > 0]
df_2 = df_2[df_2['CO2 emission (Tons)'] > 0]

# Drop columns not used in the map
df_map = df_2[['Country', 'Year', 'CO2 emission (Tons)']]  # Replace 'CO2 emission (Tons)' with your selected column
df_map = df_map.rename(columns={'CO2 emission (Tons)': 'Emissions'})
#df_map = df_map[df_map['Year'] == 2010]  # Replace 2010 with your selected year

#* Tabs with content
tab1, tab2, tab3 = st.tabs(["CO2 Map", "GDP Map", "Gemiddeldes per land"])
    
#* Map for CO2
with tab1:
    # # Check the DataFrame
    # st.subheader('DataFrame for the Map')
    # st.dataframe(df_map.head(3))
    # # Check the number of rows and unique countries
    # st.write(f"Number of Rows: {df_map.shape[0]}")
    # st.write(f"Number of Unique Countries: {len(df_map['Country'].unique())}")
    # # Filter gdf to include only countries in df_map
    # gdf = gdf[gdf['Country'].isin(df_map['Country'])]
    # # Filter gdf to include only countries in df_map
    # #df_map = df_map[df_map['Country'].isin(gdf['Country'])]
    # # Check the GeoDataFrame
    # st.subheader('GeoDataFrame for the Map')
    # #st.dataframe(gdf.head(3))
    # st.write(f"Number of Countries in GeoDataFrame: {len(gdf)}")
    
    # Create the map
    m = folium.Map(location=[0, 0], zoom_start=2)
    # Add choropleth layer
    folium.Choropleth(
        geo_data=gdf,
        name="choropleth",
        data=df_map,
        columns=["Country", "Emissions"],
        key_on="feature.properties.Country",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.1,
        legend_name="Emissions",
    ).add_to(m)
    # Display the map
    st.title('CO2 Emissions Choropleth Map')
    contact_option = df_map['Year']
    contact_selected = st.selectbox("Kies een jaar", options = contact_option )
    folium_static(m)

#* Map for GDP
with tab2:
    df_map_GDP = df_2[['Country', 'Year', 'GDP']]  # Replace 'CO2 emission (Tons)' with your selected column
    #df_map = df_map[df_map['Year'] == 2010]  # Replace 2010 with your selected year
    
    # Check the DataFrame
    # st.subheader('DataFrame for the Map')
    # st.dataframe(df_map_GDP.head(3))
    # # Check the number of rows and unique countries
    # st.write(f"Number of Rows: {df_map_GDP.shape[0]}")
    # st.write(f"Number of Unique Countries: {len(df_map_GDP['Country'].unique())}")
    # # Filter gdf to include only countries in df_map
    # gdf = gdf[gdf['Country'].isin(df_map_GDP['Country'])]
    # # Filter gdf to include only countries in df_map
    # #df_map = df_map[df_map['Country'].isin(gdf['Country'])]
    # # Check the GeoDataFrame
    # st.subheader('GeoDataFrame for the Map')
    # #st.dataframe(gdf.head(3))
    # st.write(f"Number of Countries in GeoDataFrame: {len(gdf)}")
    
    # Create the map
    m_GDP = folium.Map(location=[0, 0], zoom_start=2)
    # Add choropleth layer
    folium.Choropleth(
        geo_data=gdf,
        name="choropleth",
        data=df_map_GDP,
        columns=["Country", "GDP"],
        key_on="feature.properties.Country",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.1,
        legend_name="GDP",
    ).add_to(m_GDP)
    # Display the map
    st.title('GDP Choropleth Map')
    contact_option_GDP = df_map_GDP['Year']
    contact_selected_GDP = st.selectbox("Choose your GDP Year", options = contact_option_GDP )
    folium_static(m_GDP)

#* Mean/median by Country
with tab3:
    st.title('Country Information')
    df_3 = df_2.groupby('Country').agg({'GDP': ['mean', 'median', 'sum', 'min', 'max'], 
                                        'CO2 emission (Tons)': ['mean', 'median', 'sum', 'min', 'max']})
    df_3 = df_3.reset_index()
    contact_option_3 = df_3['Country']
    contact_selected_3 = st.selectbox("Choose your Country Year", options = contact_option_3 )
    df_3

# Sources
# st.caption('Data: CO2 Emission by countries Year wise (1750-2022), https://www.kaggle.com/datasets/moazzimalibhatti/co2-emission-by-countries-year-wise-17502022')