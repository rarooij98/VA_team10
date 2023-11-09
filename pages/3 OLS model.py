import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import statsmodels.api as sm
from statsmodels.formula.api import ols

# ---------------- SETTINGS -------------------
page_title = 'OLS model'
page_icon = '📈' # https://www.webfx.com/tools/emoji-cheat-sheet/
layout = 'wide'

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

#* Visualize model fit:
def model_fit(data, prediction_data, model):
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    # Plot the regression line and scatter points
    sns.regplot(x="Year", y="Emission", data=data, ax=axes[0, 0])
    sns.scatterplot(x="Year", y="Emission", data=prediction_data, color='red', ax=axes[0, 0])
    axes[0, 0].set_title("Prediction")
    # Residuals vs Fitted values
    residuals = model.resid
    sns.residplot(x=model.fittedvalues, y=residuals, lowess=True, line_kws={'color': 'red'}, ax=axes[0, 1])
    axes[0, 1].set_title("Residuals vs Fitted Values")
    # Q-Q plot
    sm.qqplot(residuals, fit=True, line="45", ax=axes[1, 0])
    axes[1, 0].set_title("Q-Q Plot")
    # Scale-location plot
    sns.regplot(x=model.fittedvalues, y=np.sqrt(np.abs(residuals)), ci=None, lowess=True, line_kws={'color': 'red'}, ax=axes[1, 1])
    axes[1, 1].set_title("Scale-Location Plot")
    
    # Set the layout and show the plot
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    
    st.caption('* De Q-Q plot kan worden gebruikt om te onderzoeken of de verdeling van de residuals normaal is.')
    st.caption('* De Residuals versus Fitted Values plot wordt gebruikt om niet-lineariteit en outliers te detecteren. Hiermee zie je of de residuals gelijkmatig verdeeld zijn rond de "0"-waardelijn en of de spreiding en het patroon van de punten op verschillende niveaus hetzelfde zijn.')
    st.caption('* De Scale-Location plot laat zien of de residuals gelijkmatig verdeeld zijn over de voorspelde waardes. Het is goed als je een horizontale lijn ziet met gelijkmatig (willekeurig) verspreide punten.')

#* Function to plot totals model:
def plot_model(data, prediction, model):
    # Create a scatter plot for the actual data
    fig = px.scatter(data, x="Year", y="Emission", title="Voorspelling CO2 uitstoot tot 2050", hover_data=["Year", "Emission"], trendline="ols")
    fig.update_traces(marker=dict(color="blue", symbol="circle"))
    # Create a scatter plot for the predictions with hover info
    predictions_fig = px.scatter(prediction, x="Year", y="Emission", title="Voorspelling CO2 uitstoot tot 2050", hover_data=["Year", "Emission"])
    predictions_fig.update_traces(marker=dict(color="red", symbol="square"), customdata=["Country"])
    # Add traces from predictions_fig to fig
    for trace in predictions_fig.data:
        fig.add_trace(trace)
    
    # Set the layout and show the plot
    fig.update_layout(xaxis_title="Jaar", yaxis_title="CO2 Emissies (Ton)")
    # Create 3 tabs: plot, summary & fit assessment
    tab1, tab2, tab3 = st.tabs(["Model", "Summary", "Fit"])
    with tab1:
       st.plotly_chart(fig, use_container_width=True)
    with tab2:
       st.write(model.summary())
    with tab3:
       model_fit(data, prediction, model)
    
#* Function to plot countries model:
def plot_model_countries(data, prediction):
    # Create a scatter plot for the actual data
    fig = px.scatter(data, x="Year", y="Emission", title="Voorspelling CO2 uitstoot tot 2050 per land", hover_name="Country", hover_data=["Year", "Emission"])
    fig.update_traces(marker=dict(color="blue", symbol="circle"))
    # Create a scatter plot for the predictions with hover info
    predictions_fig = px.scatter(prediction, x="Year", y="Emission", title="Voorspelling CO2 uitstoot tot 2050 per land", hover_name="Country", hover_data=["Year", "Emission"])
    predictions_fig.update_traces(marker=dict(color="red", symbol="square"), customdata=["Country"])
    # Add traces from predictions_fig to fig
    for trace in predictions_fig.data:
        fig.add_trace(trace)
    # Set the layout and show the plot
    fig.update_layout(xaxis_title="Jaar", yaxis_title="CO2 Emissies (Ton)")
    st.plotly_chart(fig, use_container_width=True)

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
    model = ols(f"{y} ~ GDP + Population", data=data).fit()
    # Make a prediction for the years 2021-2050 using the multivariable model
    explanatory_data = pd.DataFrame({"Year": np.arange(2021, 2051), "GDP": prediction_data_gdp['GDP'], "Population": prediction_data_pop['Population']})
    prediction_data = explanatory_data.assign(Emission=model.predict(explanatory_data))
    # Revert the log transformation if needed
    if (y == 'Log_Emission'):
        prediction_data['Emission'] = np.exp(prediction_data['Emission'])
    
    # Call function to plot the model
    plot_model(data, prediction_data, model)
    return prediction_data

#* Model for each country
def countries_model(data):
    # Predict the GDP for each country for the years 2021-2050
    predictions_gdp = pd.DataFrame(columns=['Country', 'Year', 'GDP'])
    years = np.arange(2021, 2051)
    for country in data['Country'].unique():
        country_data = data[data['Country'] == country]
        mdl_co2_vs_year = ols("GDP ~ Year", data=country_data).fit()
        prediction = mdl_co2_vs_year.predict(exog=pd.DataFrame({'Year': years, 'Intercept': 1}))
        country_predictions = pd.DataFrame({'Country': [country] * len(years), 'Year': years, 'GDP': prediction})
        predictions_gdp = pd.concat([predictions_gdp, country_predictions], ignore_index=True)
    
    # Predict the Population for each country for the years 2021-2050
    predictions_pop = pd.DataFrame(columns=['Country', 'Year', 'Population'])
    for country in data['Country'].unique():
        country_data = data[data['Country'] == country]
        mdl_co2_vs_year = ols("Population ~ Year", data=country_data).fit()
        prediction = mdl_co2_vs_year.predict(exog=pd.DataFrame({'Year': years, 'Intercept': 1}))
        country_predictions = pd.DataFrame({'Country': [country] * len(years), 'Year': years, 'Population': prediction})
        predictions_pop = pd.concat([predictions_pop, country_predictions], ignore_index=True)
    
    # Predict the Emission for each country for the years 2021-2050 based on Year, GDP & Population
    predictions = pd.DataFrame(columns=['Country', 'Year', 'Emission'])
    for country in data['Country'].unique():
        country_data = data[data['Country'] == country]
        gdp = predictions_gdp[predictions_gdp['Country'] == country]['GDP']
        pop = predictions_pop[predictions_pop['Country'] == country]['Population']
        mv_model_country = ols("Emission ~ GDP + Population", data=country_data).fit()
        prediction = mv_model_country.predict(exog=pd.DataFrame({'Year': years, 'GDP': gdp, 'Population': pop}))
        country_predictions = pd.DataFrame({'Country': [country] * len(years), 'Year': years, 'Emission': prediction})
        predictions = pd.concat([predictions, country_predictions], ignore_index=True)
    
    # Call function to plot the model
    plot_model_countries(data, predictions)
    return predictions
    
#* Using button inputs to call the model functions
def user_inputs():
    col1, col2 = st.columns([3, 1])
    
    # Display dropdowns
    with col2:
        model_data = st.selectbox(
        'Uitstoot data',
        ('Totaal wereldwijd', 'Per land')
        )
        if model_data == 'Totaal wereldwijd':
            model_type = st.selectbox(
                'Axis scale',
                ('Lineair', 'Logaritmisch')
            )
    
    # Display models conditionally
    with col1:
        if model_data == 'Totaal wereldwijd':
            if model_type == 'Lineair':
                create_mv_model(total_data, 'Emission')
            elif model_type == 'Logaritmisch':
                create_mv_model(total_data, 'Log_Emission')
        elif model_data == 'Per land':
                countries_model(df_mv)

user_inputs()

# Sources
# st.caption('Data: CO2 Emission by countries Year wise (1750-2022), https://www.kaggle.com/datasets/moazzimalibhatti/co2-emission-by-countries-year-wise-17502022')