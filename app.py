# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 10:52:55 2024

@author: aspirex99
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import json

# Load GeoJSON data for Indian states
@st.cache
def load_geojson():
    with open(r"C:\Users\aspir\Downloads\MAPPING TASK\states_india.geojson", "r") as file:
        return json.load(file)

# Load CSV data
@st.cache
def load_data():
    return pd.read_csv(r"C:\Users\aspir\Downloads\MAPPING TASK\Real_Districts_Data_for_Indian_States.csv")

# Streamlit app
st.title("Interactive Choropleth Map for Indian States")
st.write("Visualize retail data across Indian states with an interactive map.")

# Load data
india_states = load_geojson()
df = load_data()

# Create a state-to-ID mapping
state_id_map = {}
for feature in india_states['features']:
    feature['id'] = feature['properties']['state_code']
    state_id_map[feature['properties']['st_nm']] = feature['id']

# Add 'id' column to dataframe
df['id'] = df['State'].apply(lambda x: state_id_map.get(x, None))

# Add dropdown for color scale selection
color_scale = st.selectbox(
    "Select Color Scale",
    options=["Viridis", "Cividis", "Plasma", "Inferno", "Turbo"]
)

# Create choropleth map
fig = px.choropleth(
    df,
    locations='id',
    geojson=india_states,
    color="Retail Count",
    scope="asia",
    hover_name="State",
    hover_data=["Retail Count", "Retailers with QR Code"],
    color_continuous_scale=color_scale
)

fig.update_geos(fitbounds='locations', visible=False)

# Display the map
st.plotly_chart(fig, use_container_width=True)

st.write("Use the dropdown above to select different color scales for the map visualization.")
