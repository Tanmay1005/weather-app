const API_KEY = 'YOUR_API_KEY'; // Replace with your OpenWeatherMap API key

function getWeather() {
    const city = document.getElementById('cityInput').value;
    if (city) {
        fetchWeatherData(city);
        fetchForecastData(city);
        fetchWeatherAlerts(city);
    } else {
        showError('Please enter a city name');
    }
}

function fetchWeatherData(city) {
    const url = `http://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${API_KEY}&units=metric`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.cod === 200) {
                displayWeather(data);
                displayClothingRecommendations(data.main.temp, data.weather[0].description, data.wind.speed);
            } else {
                showError('City not found');
            }
        })
        .catch(() => showError('An error occurred while fetching weather data'));
}

function fetchForecastData(city) {
    const url = `http://api.openweathermap.org/data/2.5/forecast?q=${city}&appid=${API_KEY}&units=metric`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.cod === '200') {
                displayForecast(data.list);
            } else {
                showError('Forecast data not found');
            }
        })
        .catch(() => showError('An error occurred while fetching forecast data'));
}

function fetchWeatherAlerts(city) {
    const url = `http://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${API_KEY}&units=metric`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            displayAlerts(data.alerts || []);
        })
        .catch(() => showError('An error occurred while fetching weather alerts'));
}

function displayWeather(data) {
    const unit = document.querySelector('input[name="tempUnit"]:checked').value;
    const temp = convertTemperature(data.main.temp, unit);
    const feelsLike = convertTemperature(data.main.feels_like, unit);
    
    const weatherInfo = document.getElementById('weatherInfo');
    weatherInfo.innerHTML = `
        <h2>Weather in ${data.name}</h2>
        <p><strong>Temperature:</strong> ${temp}°${unit}</p>
        <p><strong>Feels Like:</strong> ${feelsLike}°${unit}</p>
        <p><strong>Weather:</strong> ${data.weather[0].description}</p>
        <img src="http://openweathermap.org/img/wn/${data.weather[0].icon}@2x.png" alt="${data.weather[0].description}">
        <p><strong>Humidity:</strong> ${data.main.humidity}%</p>
        <p><strong>Wind Speed:</strong> ${data.wind.speed} m/s</p>
    `;
}

function displayForecast(forecastList) {
    const unit = document.querySelector('input[name="tempUnit"]:checked').value;
    const forecastInfo = document.getElementById('forecastInfo');
    forecastInfo.innerHTML = '<h2>5-Day Forecast</h2>';
    
    const days = {};

    forecastList.forEach(entry => {
        const date = new Date(entry.dt_txt);
        const day = date.toLocaleDateString(undefined, { weekday: 'long', month: 'short', day: 'numeric' });
        if (!days[day]) {
            days[day] = [];
        }
        days[day].push({
            time: date.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' }),
            temp: convertTemperature(entry.main.temp, unit),
            description: entry.weather[0].description,
            icon: entry.weather[0].icon
        });
    });

    for (const [day, entries] of Object.entries(days)) {
        const dayDiv = document.createElement('div');
        dayDiv.classList.add('forecast-day');
        dayDiv.innerHTML = `<h3>${day}</h3>`;
        entries.forEach(entry => {
            const entryDiv = document.createElement('div');
            entryDiv.innerHTML = `
                <p><strong>${entry.time}</strong></p>
                <p>${entry.temp}°${unit}</p>
                <img src="http://openweathermap.org/img/wn/${entry.icon}@2x.png" alt="${entry.description}">
                <p>${entry.description}</p>
            `;
            dayDiv.appendChild(entryDiv);
        });
        forecastInfo.appendChild(dayDiv);
    }
}

function convertTemperature(tempCelsius, unit) {
    if (unit === 'F') {
        return (tempCelsius * 9/5 + 32).toFixed(1);
    }
    return tempCelsius.toFixed(1);
}

function displayAlerts(alerts) {
    const alertInfo = document.getElementById('alertInfo');
    alertInfo.innerHTML = '<h2>Weather Alerts</h2>';
    
    if (alerts.length > 0) {
        alerts.forEach(alert => {
            alertInfo.innerHTML += `
                <div class="alert">
                    <p><strong>${alert.event}</strong></p>
                    <p>Start: ${new Date(alert.start * 1000).toLocaleString()}</p>
                    <p>End: ${new Date(alert.end * 1000).toLocaleString()}</p>
                    <p>${alert.description}</p>
                </div>
            `;
        });
    } else {
        alertInfo.innerHTML += '<p>No weather alerts at this time.</p>';
    }
}

function displayClothingRecommendations(temp, description, windSpeed) {
    const unit = document.querySelector('input[name="tempUnit"]:checked').value;
    const clothingReco = document.getElementById('clothingReco');
    clothingReco.innerHTML = '<h2>Clothing Recommendations</h2>';

    const recommendations = [];

    // Temperature-based recommendations
    if (unit === 'F') temp = (temp - 32) * 5/9; // Convert to Celsius for recommendation logic

    if (temp > 30) {
        recommendations.push("Wear light and breathable clothing (e.g., t-shirt, shorts).");
        recommendations.push("Stay hydrated and avoid direct sunlight.");
    } else if (20 <= temp <= 30) {
        recommendations.push("Wear comfortable clothing (e.g., t-shirt, jeans).");
    } else if (10 <= temp < 20) {
        recommendations.push("Wear a light jacket or sweater.");
    } else if (0 <= temp < 10) {
        recommendations.push("Wear a warm jacket, scarf, and gloves.");
    } else {
        recommendations.push("Wear heavy winter clothing, including a coat, hat, gloves, and scarf.");
        recommendations.push("Consider layering up to stay warm.");
    }

    // Weather condition-based recommendations
    if (description.includes('rain')) {
        recommendations.push("Carry an umbrella or wear a raincoat.");
        recommendations.push("Wear waterproof footwear.");
    } else if (description.includes('snow')) {
        recommendations.push("Wear snow boots and a warm hat.");
        recommendations.push("Consider wearing layers to stay warm.");
    }

    // Wind speed-based recommendations
    if (windSpeed > 15) {
        recommendations.push("It's windy, so wear something windproof.");
    }

    clothingReco.innerHTML += recommendations.map(rec => `<p>- ${rec}</p>`).join('');
}

function showError(message) {
    const weatherInfo = document.getElementById('weatherInfo');
    weatherInfo.innerHTML = `<p class="error">${message}</p>`;
}
