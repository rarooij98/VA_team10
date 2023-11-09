import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st
import plotly.express as px
import geopandas as gpd
import folium
from streamlit_folium import folium_static


df = pd.read_csv('data\df.csv')
gdf = gpd.read_file('VA_team10\countries.geojson')
World = pd.read_csv('data\world_country_and_usa_states_latitude_and_longitude_values (1).csv')
World = World.rename(columns={'country': 'Country'})
World_selec = World[['Country', 'latitude', 'longitude']]
World_selec
# Rename 'United States of America' to 'United States'
df['Country'] = df['Country'].replace({'United States' : 'United States of America'})

gdf = gdf.rename(columns={'ADMIN' : 'Country'})

df_2 = df.loc[df['GDP'] > 0]
df_2 = df_2[df_2['Population(2022)'] > 0]
df_2 = df_2[df_2['Area'] > 0]
df_2 = df_2[df_2['CO2 emission (Tons)'] > 0]

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
st.title('Country Information')
df_3_option = df_3['Country']
df_3_selected = st.selectbox("Which Country would you like to choose?",
                              options=df_3_option.tolist(),
                              index=1)

selected_country_data = df_3[df_3['Country'] == df_3_selected]
st.write(selected_country_data)

# Drop columns not used in the map
df_map = df_2[['Country', 'Year', 'CO2 emission (Tons)']]  # Replace 'CO2 emission (Tons)' with your selected column
df_map = df_map.rename(columns={'CO2 emission (Tons)': 'Emissions'})
#df_map = df_map[df_map['Year'] == 2010]  # Replace 2010 with your selected year

# Check the DataFrame
st.subheader('DataFrame for the Map')
st.dataframe(df_map.head(3))

# Check the number of rows and unique countries
st.write(f"Number of Rows: {df_map.shape[0]}")
st.write(f"Number of Unique Countries: {len(df_map['Country'].unique())}")


# Filter gdf to include only countries in df_map
gdf = gdf[gdf['Country'].isin(df_map['Country'])]

# Filter gdf to include only countries in df_map
#df_map = df_map[df_map['Country'].isin(gdf['Country'])]

# Check the GeoDataFrame
st.subheader('GeoDataFrame for the Map')
st.write(f"Number of Countries in GeoDataFrame: {len(gdf)}")

# Convert 'Year' column to string if needed
df_map['Year'] = df_map['Year'].sort_values(ascending=True).astype(str)

# Options for Selectbox
contact_option = df_map['Year'].unique()
contact_selected = st.selectbox("Choose your Emissions Year", options=contact_option)

# Filter DataFrame based on selected year
filtered_df = df_map[df_map['Year'] == contact_selected]

# Create the map
m = folium.Map(location=[0, 0], zoom_start=2)

# Add choropleth layer
folium.Choropleth(
    geo_data=gdf,
    name="choropleth",
    data=filtered_df,
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




df_map_GDP = df_2[['Country', 'Year', 'GDP']]  # Replace 'CO2 emission (Tons)' with your selected column
#df_map = df_map[df_map['Year'] == 2010]  # Replace 2010 with your selected year

# Check the DataFrame
st.subheader('DataFrame for the Map')
st.dataframe(df_map_GDP.head(3))

# Check the number of rows and unique countries
st.write(f"Number of Rows: {df_map_GDP.shape[0]}")
st.write(f"Number of Unique Countries: {len(df_map_GDP['Country'].unique())}")

# Convert 'Year' column to string if needed
df_map_GDP['Year'] = df_map_GDP['Year'].sort_values(ascending=True).astype(str)

# Options for Selectbox
contact_option_GDP = df_map_GDP['Year'].unique().astype(str)
contact_selected_GDP = st.selectbox("Choose your GDP Year", options=contact_option_GDP)

# Filter DataFrame based on selected year
filtered_df_GDP = df_map_GDP[df_map_GDP['Year'] == contact_selected_GDP]

# Filter gdf to include only countries in df_map_GDP
gdf = gdf[gdf['Country'].isin(filtered_df_GDP['Country'])]

# Create the map
m_GDP = folium.Map(location=[0, 0], zoom_start=2)

# Add choropleth layer
folium.Choropleth(
    geo_data=gdf,
    name="choropleth",
    data=filtered_df_GDP,
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