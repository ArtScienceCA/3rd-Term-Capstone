import streamlit as st
import pandas as pd
import plotly.express as px


# Load the data
confirmed_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
confirmed_df = pd.read_csv(confirmed_url)

# Data processing (melt the dataframe for easier plotting)
confirmed_df = confirmed_df.melt(
    id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
    var_name='Date',
    value_name='Confirmed'
)
confirmed_df['Date'] = pd.to_datetime(confirmed_df['Date'])

# Streamlit app
st.title("COVID-19 Case Tracker")

# Country selection
countries = confirmed_df['Country/Region'].unique()
selected_country = st.selectbox("Select a Country", countries)

# Display Type selection
display_type = st.radio("Display Type", ('Daily Cases', 'Cumulative Cases'))

# Filter data by selected country
country_data = confirmed_df[confirmed_df['Country/Region'] == selected_country]

# Group by date (in case there are multiple rows for the same country)
country_data = country_data.groupby('Date', as_index=False)['Confirmed'].sum()

# Calculate daily cases
country_data['Daily Cases'] = country_data['Confirmed'].diff()

# Plotting
if display_type == 'Daily Cases':
    fig = px.line(
        country_data,
        x='Date',
        y='Daily Cases',
        title=f'Daily COVID-19 Cases in {selected_country}',
        labels={'Daily Cases': 'Number of Cases', 'Date': 'Date'}
    )
elif display_type == 'Cumulative Cases':
    fig = px.line(
    
        country_data,
        x='Date',
        y='Confirmed',
        title=f'Cumulative COVID-19 Cases in {selected_country}',
        labels={'Confirmed': 'Number of Cases', 'Date': 'Date'}
    )

# Display the plotss
st.plotly_chart(fig)

# Display raw data (optional)
if st.checkbox("Show Raw Data"):
    st.write(country_data)