import streamlit as st
from utils.weather import get_weather, get_forecast, get_alerts, get_clothing_recommendations
from datetime import datetime
from geopy.geocoders import Nominatim

def convert_temperature(temp_celsius, unit):
    if unit == "Fahrenheit":
        return temp_celsius * 9/5 + 32
    return temp_celsius

st.title("🌤️ Weather App")

st.sidebar.title("Options")

unit = st.sidebar.radio("Select Temperature Unit:", ("Celsius", "Fahrenheit"))
show_forecast = st.sidebar.checkbox("Show 5-Day Forecast")
show_alerts = st.sidebar.checkbox("Show Weather Alerts")

show_clothing_recommendations = st.sidebar.checkbox("Show Clothing Recommendations")

city = st.text_input("Enter a city name:")

if city:
    weather_data = get_weather(city)
    forecast_data = get_forecast(city) if show_forecast else None
    
    
    if weather_data:
        temp = convert_temperature(weather_data['temp'], unit)
        feels_like = convert_temperature(weather_data['feels_like'], unit)
        
        st.subheader(f"Weather in {city.capitalize()}:")
        st.write(f"**Temperature:** {temp:.2f}°{unit[0]}")
        st.write(f"**Feels Like:** {feels_like:.2f}°{unit[0]}")
        st.write(f"**Weather:** {weather_data['description'].capitalize()}")
        st.write(f"**Humidity:** {weather_data['humidity']}%")
        st.write(f"**Wind Speed:** {weather_data['wind_speed']} m/s")

        # Display the weather icon
        icon_url = f"http://openweathermap.org/img/wn/{weather_data['icon']}@2x.png"
        st.image(icon_url, caption=weather_data['description'].capitalize())

        # Display clothing recommendations
        if show_clothing_recommendations:
            st.subheader("Clothing Recommendations")
            recommendations = get_clothing_recommendations(temp, weather_data['description'], weather_data['wind_speed'])
            for rec in recommendations:
                st.write(f"- {rec}")


    
    if show_forecast and forecast_data:
        st.subheader("5-Day Forecast")
        
        # Organize forecast data by day
        forecast_by_day = {}
        for entry in forecast_data:
            dt = datetime.strptime(entry['datetime'], "%Y-%m-%d %H:%M:%S")
            day = dt.strftime('%A, %b %d')
            if day not in forecast_by_day:
                forecast_by_day[day] = []
            forecast_by_day[day].append(entry)
        
        # Display forecast data horizontally for each day
        for day, entries in forecast_by_day.items():
            st.markdown(f"**{day}**")
            cols = st.columns(len(entries))
            for i, entry in enumerate(entries):
                with cols[i]:
                    st.write(f"**{datetime.strptime(entry['datetime'], '%Y-%m-%d %H:%M:%S').strftime('%I:%M %p')}**")
                    temp = convert_temperature(entry['temp'], unit)
                    st.write(f"{temp:.2f}°{unit[0]}")
                    st.image(f"http://openweathermap.org/img/wn/{entry['icon']}@2x.png", width=50)
                    st.write(entry['description'].capitalize())
    elif show_forecast:
        st.error("Forecast data could not be retrieved.")
    


    if show_alerts:
        alerts = get_alerts(city)
        if alerts:
          st.subheader("Weather Alerts")
          for alert in alerts:
            st.write(f"**{alert['event']}**")
            st.write(f"Start: {datetime.fromtimestamp(alert['start']).strftime('%Y-%m-%d %H:%M:%S')}")
            st.write(f"End: {datetime.fromtimestamp(alert['end']).strftime('%Y-%m-%d %H:%M:%S')}")
            st.write(f"Description: {alert['description']}")
            st.write("---")
        else:
            st.subheader("No weather alerts at this time.")

else:
    st.error("City not found or API error")

st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 40px;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        text-align: center;
        padding: 5px;
    }
    </style>
    <div class="footer">
        <p>Made by Tanmay Ambegaokar</p>
        <p> The Product Manager Accelerator Program is designed to support PM professionals through every stage of their career.
         
    </div>
    """, unsafe_allow_html=True)