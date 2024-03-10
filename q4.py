import streamlit as st
import pandas as pd
import plotly.express as px

# Correctly using st.cache_data for caching the dataset loading and processing
@st.cache_data(ttl=None, show_spinner=True, persist="disk", experimental_allow_widgets=False)
def load_data():
    file_path = 'weather - 286_40.75_t2m_1d.csv'  # Update this path as necessary
    data = pd.read_csv(file_path)
    data['time'] = pd.to_datetime(data['time'])
    data['Ftemp'] = (data['Ktemp'] - 273.15) * 9/5 + 32
    data['year'] = data['time'].dt.year
    data['month'] = data['time'].dt.month
    return data

data = load_data()

# Part A: Interactive Monthly Average Temperature Visualization
st.header("Part A: Monthly Average Temperature")
min_year, max_year = int(data['year'].min()), int(data['year'].max())
selected_year = st.slider('Select a Year', min_year, max_year, min_year)
filtered_data_year = data[data['year'] == selected_year].groupby(['month'])['Ftemp'].mean().reset_index()
fig_monthly = px.line(filtered_data_year, x='month', y='Ftemp', title=f'Average Monthly Temperature in {selected_year}')
st.plotly_chart(fig_monthly)

# Part B: First Year Above 55°F
st.header("Part B: First Year with Average Temperature Above 55°F")
annual_avg_temp = data.groupby('year')['Ftemp'].mean()
first_year_above_55 = annual_avg_temp[annual_avg_temp > 55].index[0]
st.write(f"The first year where the average temperature was above 55°F is: {first_year_above_55}")

# Part C: Creative Visualization - Seasonal Trends
st.header("Part C: Seasonal Temperature Trends Over Years")
def month_to_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

data['season'] = data['month'].apply(month_to_season)
seasonal_avg_temp = data.groupby(['year', 'season'])['Ftemp'].mean().reset_index()
fig_seasonal = px.line(seasonal_avg_temp, x='year', y='Ftemp', color='season', title='Seasonal Temperature Trends Over Years')
st.plotly_chart(fig_seasonal)
