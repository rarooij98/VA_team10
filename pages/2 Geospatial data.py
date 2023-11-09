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
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

df = load_data("./data/df.csv")
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
df_map = df_2[['Country', 'Year', 'CO2 emission (Tons)']]
df_map = df_map.rename(columns={'CO2 emission (Tons)': 'Emissions'})

#* Map for CO2
def co2_map(gdf, df_map):
    # Filter gdf to include only countries in df_map
    gdf = gdf[gdf['Country'].isin(df_map['Country'])]
    # Create the map
    m = folium.Map(location=[0, 0], zoom_start=2)
    # Choose Year
    contact_option = df_map['Year']
    contact_selected = st.selectbox("Kies een jaar", options=contact_option, key="CO2", index=40)
    df_map = df_map[df_map['Year']==contact_selected]
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
    folium_static(m)

#* Map for GDP
def gdp_map(gdf):
        df_map_GDP = df_2[['Country', 'Year', 'GDP']]
        # Filter gdf to include only countries in df_map
        gdf = gdf[gdf['Country'].isin(df_map_GDP['Country'])]
        # Choose Year
        contact_option_GDP = df_map_GDP['Year']
        contact_selected_GDP = st.selectbox("Kies een jaar", options=contact_option_GDP, key="GDP", index=40)
        df_map = df_map_GDP[df_map_GDP['Year']==contact_selected_GDP]
        # Create the map
        m_GDP = folium.Map(location=[0, 0], zoom_start=2)
        # Add choropleth layer
        folium.Choropleth(
            geo_data=gdf,
            name="choropleth",
            data=df_map,
            columns=["Country", "GDP"],
            key_on="feature.properties.Country",
            fill_color="YlOrRd",
            fill_opacity=0.7,
            line_opacity=0.1,
            legend_name="GDP",
        ).add_to(m_GDP)
        # Display the map
        st.title('GDP Choropleth Map')
        folium_static(m_GDP)

#* Mean/median by Country
def get_mean(df_2):
        st.title('Country Information')
        df_3 = df_2.groupby('Country').agg({'GDP': ['mean', 'median', 'sum', 'min', 'max'], 
                                            'CO2 emission (Tons)': ['mean', 'median', 'sum', 'min', 'max']})
        df_3 = df_3.reset_index()
        df_3.columns = [' '.join(col).strip() for col in df_3.columns.values]
        df_3 = df_3.rename(columns={'Country, ': 'Country',
                                    ('GDP', 'mean'): 'GDP_mean',
                                    ('GDP', 'median'): 'GDP_median',
                                    ('GDP', 'sum'): 'GDP_sum',
                                    ('GDP', 'min'): 'GDP_min',
                                    ('GDP', 'max'): 'GDP_max',
                                    ('CO2 emission (Tons)', 'mean'): 'Emission_mean',
                                    ('CO2 emission (Tons)', 'median'): 'Emission_median',
                                    ('CO2 emission (Tons)', 'sum'): 'Emission_sum',
                                    ('CO2 emission (Tons)', 'min'): 'Emission_min',
                                    ('CO2 emission (Tons)', 'max'): 'Emission_max'})
        
        # Display filtered dataset
        contact_option_3 = df_3['Country']
        contact_selected_3 = st.selectbox("Kies een jaar", options=contact_option_3, key="mean")
        df_3[df_3['Country']==contact_selected_3]

#* Tabs with content
tab1, tab2, tab3 = st.tabs(["CO2 Map", "GDP Map", "Gemiddeldes per land"])
with tab1:
    co2_map(gdf, df_map)
with tab2:
    gdp_map(gdf)
with tab3:
    get_mean(df_2)
    
# Sources
# st.caption('Data: CO2 Emission by countries Year wise (1750-2022), https://www.kaggle.com/datasets/moazzimalibhatti/co2-emission-by-countries-year-wise-17502022')