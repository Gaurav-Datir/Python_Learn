import chainlit as cl

@cl.on_chat_start
async def start():
    # We explicitly set the author to "HealthPal" for the bot
    content = "Hi, I'm HealthPal... I can help you check symptoms or find a doctor."
    await cl.Message(content=content, author="HealthPal").send()

@cl.on_message
async def main(message: cl.Message):
    # message.author is automatically "You" by default in Chainlit
    if "symptoms" in message.content.lower():
        await cl.Message(
            content="Sure. To start... how long you've had these symptoms?",
            author="HealthPal"
        ).send()
    else:
        await cl.Message(content="I'm here to help!", author="HealthPal").send()