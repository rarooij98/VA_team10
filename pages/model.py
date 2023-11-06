import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns
import plotly.express as px
from statsmodels.formula.api import ols

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
df_mv = pd.read_csv("./data/df_mv.csv")
total_data = pd.read_csv("./data/total_data.csv")

# ----------------- PAGES ---------------------
st.title(page_title + ' ' + page_icon)

#* Create DataFrame
df_ols = CO2.rename(columns={'CO2 emission (Tons)': 'Emission'})
df_ols = df_ols[df_ols['Year'] > 1959] # data from 1960-2020

# Create a DataFrame with the total emissions for each year
total_emissions = df_ols.groupby('Year')['Emission'].sum()
total_emissions = total_emissions.reset_index()
total_emissions.columns = ['Year', 'Emission']
total_emissions['Log_Emission'] = np.log(total_emissions['Emission'])

#* Function to plot each model:
def plot_model(data, prediction):
    # Create a scatter plot for the actual data
    fig = px.scatter(data, x="Year", y="Emission", title="Predictie totale CO2 emissies tot 2050", hover_data=["Year", "Emission"], trendline="ols")
    fig.update_traces(marker=dict(color="blue", symbol="circle"))
    # Create a scatter plot for the predictions with hover info
    predictions_fig = px.scatter(prediction, x="Year", y="Emission", title="Predictie totale CO2 emissies tot 2050", hover_data=["Year", "Emission"])
    predictions_fig.update_traces(marker=dict(color="red", symbol="square"), customdata=["Country"])
    # Add traces from predictions_fig to fig
    for trace in predictions_fig.data:
        fig.add_trace(trace)
    # Set the layout and show the plot
    fig.update_layout(xaxis_title="Jaar", yaxis_title="CO2 Emissies (Tons)")
    st.plotly_chart(fig, use_container_width=True)

#* Simple model
# def create_model(data, y):
#     # With this DataFrame, create a model that predicts the total emissions for the years 2021-2050
#     model = ols(f"{y} ~ Year", data=data).fit()
#     # Make a prediction for the years 2021-2050 using the model
#     explanatory_data = pd.DataFrame({"Year": np.arange(2021, 2051)})
#     prediction_data = explanatory_data.assign(Emission=model.predict(explanatory_data))
#     # Revert the log transformation if needed
#     if (y == 'Log_Emission'):
#         prediction_data['Emission'] = np.exp(prediction_data['Emission'])
    
#     # Call function to plot the model
#     plot_model(data, prediction_data)
#     return prediction_data

# create_model(total_emissions, 'Emission')
# create_model(total_emissions, 'Log_Emission')

#* Multivariable model
def create_mv_model(data, y):
    # Predict the total GDP for the years 2021-2050
    mdl_gdp = ols("GDP ~ Year", data=data).fit()
    explanatory_data_gdp = pd.DataFrame({"Year": np.arange(2021, 2051)})
    prediction_data_gdp = explanatory_data_gdp.assign(GDP=mdl_gdp.predict(explanatory_data_gdp))
    # Predict the total Population for the years 2021-2050
    mdl_pop = ols("Population ~ Year", data=data).fit()
    explanatory_data_pop = pd.DataFrame({"Year": np.arange(2021, 2051)})
    prediction_data_pop = explanatory_data_pop.assign(Population=mdl_pop.predict(explanatory_data_pop))

    # Create a multivariable model with the GDP & Population predictions
    mv_model = ols(f"{y} ~ Year + GDP + Population", data=data).fit()
    # Make a prediction for the years 2021-2050 using the multivariable model
    explanatory_data = pd.DataFrame({"Year": np.arange(2021, 2051), "GDP": prediction_data_gdp['GDP'], "Population": prediction_data_pop['Population']})
    prediction_data = explanatory_data.assign(Emission=mv_model.predict(explanatory_data))
    # Revert the log transformation if needed
    if (y == 'Log_Emission'):
        prediction_data['Emission'] = np.exp(prediction_data['Emission'])
    
    # Call function to plot the model
    plot_model(data, prediction_data)
    return prediction_data
    
#* Calling the model functions conditionally with button inputs
col1, col2 = st.columns([3, 1])

with col2:
    #~ Display buttons
   model_lin = st.button("Lineair", type="primary")
   model_log = st.button("Logaritmic", type="primary")

with col1:
    #~ Display models
    if model_lin:
        create_mv_model(total_data, 'Emission')
    if model_log:
        create_mv_model(total_data, 'Log_Emission')
    else:
        create_mv_model(total_data, 'Emission') #? Default option
    
# create_mv_model(total_data, 'Emission')
# create_mv_model(total_data, 'Log_Emission')