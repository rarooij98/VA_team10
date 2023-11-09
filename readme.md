# CO2 uitstoot & GDP
In deze Streamlit app onderzoeken we de CO2 emissies van landen over de jaren heen, en vergelijken de emissies van een land met het GDP. 
         Welke landen stoten het meeste CO2 uit, hebben zij een hoger GDP? We gebruiken een lineair 
         regressie model om de uitstoot voor komende jaren te voorspellen aan de hand van de GDP en Population van landen.

## Prerequisites

List any prerequisites or dependencies that users need to have installed before they can use your project. Include versions if necessary.

- Python 3.11
- streamlit 1.27.0
- pandas 2.1.1
- numpy 1.26.0
- matplotlib 3.8.0
- seaborn 0.12.2
- python-dotenv 1.0.0
- plotly 5.17.0
- geopandas 0.14
- folium 0.14.0
- streamlit_folium 0.15.0
- statsmodels 0.14.0

## Getting Started

### Installation

1. Clone the repository to your local machine:
2. Navigate to the project directory:
3. Create a virtual environment (recommended):
```bash
python -m venv venv
```
4. Activate the virtual environment:
- On Windows:
```bash
venv\Scripts\activate
```
- On macOS and Linux:
```bash
source venv/bin/activate
```
5. Install project dependencies from requirements.txt:
```bash
pip install -r requirements.txt
```
6. Explain how to use your project once it's set up. Provide examples and usage instructions.
```bash
streamlit run app.py
```

## Column Explanations

Here is a breakdown of the columns in the dataset:

* "Country": Name of Country
* "Code": ISO alpha-3 calling code of every country
* "Year": Year of CO2 emission / GDP
* "GDP": GDP of every country
* "Calling Code": Calling code of every country
* "CO2 emission (Tons)": Amount of CO2 emission in Tons
* "Area": Area of that country in km2
* "% of World": How much % of World landmass, this country covered
* "Density(km2)": Density according to Area in km2