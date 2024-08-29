# Weather App using Streamlit

This is a simple weather app built using Python and Streamlit. The app allows users to enter a city name and get the current weather information.

## Features
- Get current weather details for any city.
- (Optional) View a 5-day weather forecast.
- (Optional) Get weather based on your current location.
- Weather icons for better visualization.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/weather-app-streamlit.git
   cd weather-app-streamlit
2. Install dependencies
    ```bash
    pip install -r requirements.txt
3. Get your API key from OpenWeatherMap and add it to config.py and script.js
4. Run the app:
    ```bash
    streamlit run src/app.py

5. Additionally if you want to test the app made on JS, run index.html file

## How to get OpenWeatherMap API key

1. Create an account on OpenWeatherMap (https://openweathermap.org/)
2. Create an API key for free and save it.
3. Paste the API key in config.py and script.js files for the apps to run.

