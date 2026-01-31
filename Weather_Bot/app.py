import os
import requests
import chainlit as cl
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

# -------------------------------
# Chat start message
# -------------------------------
@cl.on_chat_start
async def start():
    await cl.Message(
        content=(
            "🌤️ **Welcome to Weather App!**\n\n"
            "Type a **city name** to get the current weather."
        ),
        author="WeatherBot"
    ).send()


# -------------------------------
# Handle user messages
# -------------------------------
@cl.on_message
async def get_weather(message: cl.Message):
    city = message.content.strip()

    # Validate input
    if not city:
        await cl.Message(
            content="❌ Please enter a valid city name.",
            author="WeatherBot"
        ).send()
        return

    # OpenWeather API URL
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        await cl.Message(
            content="⚠️ Unable to fetch weather data. Please try again.",
            author="WeatherBot"
        ).send()
        return

    data = response.json()

    # Extract weather data
    weather_desc = data["weather"][0]["description"].title()
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]

    # Response message (formatted for chat bubble UI)
    result = (
        f"🌍 **City:** {city.title()}\n"
        f"🌡 **Temperature:** {temp}°C\n"
        f"🤒 **Feels Like:** {feels_like}°C\n"
        f"💧 **Humidity:** {humidity}%\n"
        f"☁️ **Weather:** {weather_desc}"
    )

    await cl.Message(
        content=result,
        author="WeatherBot"
    ).send()
