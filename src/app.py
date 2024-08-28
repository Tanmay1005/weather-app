import streamlit as st
from utils.weather import get_weather

st.title("Weather App")

city = st.text_input("Enter a city name:")

if city:
    weather_data = get_weather(city)
    if weather_data:
        st.write(weather_data)
    else:
        st.error("City not found or API error")