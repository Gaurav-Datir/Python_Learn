import os
import requests
import chainlit as cl
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("") # Replace with your actual environment variable name
cl
@cl.on_chat_start
async def start():
    await cl.Message(
        content="🌤️ Welcome to Weather App!\n\nType a city name to get current weather."
    ).send()

@cl.on_message
async def get_weather(message: cl.Message):
    city = message.content.strip()

    if not city:
        await cl.Message(content="❌ Please enter a valid city name.").send()
        return

    url = (
        f"" # OpenWeatherMap API endpoint
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)

    if response.status_code != 200:
        await cl.Message(
            content="⚠️ City not found. Please try another city."
        ).send()
        return

    data = response.json()

    weather = data["weather"][0]["description"].title()
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]

    result = f"""
🌍 **City:** {city.title()}
🌡 **Temperature:** {temp}°C
🤒 **Feels Like:** {feels_like}°C
💧 **Humidity:** {humidity}%
☁️ **Weather:** {weather}
"""

    await cl.Message(content=result).send()

