import chainlit as cl
from datetime import datetime

# Sample healthcare knowledge base
HEALTH_KB = {
    "fever": {
        "info": "A fever is a temporary increase in body temperature, often due to illness. Normal body temperature is around 98.6°F (37°C).",
        "symptoms": "Sweating, chills, headache, muscle aches, weakness",
        "care": "Rest, stay hydrated, take fever reducers like acetaminophen if recommended. Seek medical attention if fever exceeds 103°F (39.4°C) or lasts more than 3 days."
    },
    "headache": {
        "info": "Headaches are common and can be caused by stress, dehydration, eye strain, or other factors.",
        "symptoms": "Pain in head, pressure, throbbing sensation",
        "care": "Rest in a quiet dark room, stay hydrated, apply cold or warm compress. If severe or persistent, consult a doctor."
    },
    "cold": {
        "info": "The common cold is a viral infection of the upper respiratory tract.",
        "symptoms": "Runny nose, sore throat, cough, sneezing, mild fever",
        "care": "Rest, drink fluids, use saline nasal drops. Most colds resolve in 7-10 days."
    },
    "cough": {
        "info": "A cough is a reflex that helps clear airways of mucus and irritants.",
        "symptoms": "Persistent coughing, chest discomfort, may produce mucus",
        "care": "Stay hydrated, use honey (for adults), avoid irritants. See a doctor if cough persists over 3 weeks or includes blood."
    }
}

EMERGENCY_KEYWORDS = ["chest pain", "difficulty breathing", "severe bleeding", 
                      "unconscious", "stroke", "heart attack", "suicide", 
                      "overdose", "seizure"]

@cl.on_chat_start
async def start():
    """Initialize the chatbot when a user connects"""
    await cl.Message(
        content="""# 🏥 Welcome to Healthcare Assistant

I'm here to provide general health information and guidance. 
**I can help with:**
- General health information
- Common symptoms and self-care tips
- When to see a doctor
- Healthy lifestyle advice

How can I assist you today?"""
    ).send()
    
    # Store conversation history
    cl.user_session.set("history", [])

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages"""
    user_msg = message.content.lower()
    
    # Check for emergency keywords
    if any(keyword in user_msg for keyword in EMERGENCY_KEYWORDS):
        await cl.Message(
            content="""🚨 **EMERGENCY ALERT** 🚨

Your message suggests a potential medical emergency. 

**Please take immediate action:**
- Call 911 (US) or your local emergency number
- Go to the nearest emergency room
- Contact your doctor immediately

This chatbot cannot handle emergencies. Please seek immediate professional help."""
        ).send()
        return
    
    # Get conversation history
    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content, "timestamp": datetime.now()})
    
    # Generate response
    response = generate_response(user_msg)
    
    # Add disclaimer
    disclaimer = "\n\n---\n*This information is for general guidance only. Please consult a healthcare professional for personalized medical advice.*"
    full_response = response + disclaimer
    
    # Send response
    await cl.Message(content=full_response).send()
    
    # Update history
    history.append({"role": "assistant", "content": response, "timestamp": datetime.now()})
    cl.user_session.set("history", history)

def generate_response(user_input):
    """Generate appropriate response based on user input"""
    
    # Greeting responses
    if any(greet in user_input for greet in ["hello", "hi", "hey", "greetings"]):
        return "Hello! How can I help you with your health questions today?"
    
    # Check knowledge base
    for condition, info in HEALTH_KB.items():
        if condition in user_input:
            response = f"**About {condition.title()}:**\n\n"
            response += f"{info['info']}\n\n"
            response += f"**Common Symptoms:** {info['symptoms']}\n\n"
            response += f"**Self-Care Tips:** {info['care']}"
            return response
    
    # General health questions
    if "when" in user_input and "doctor" in user_input:
        return """**When to See a Doctor:**

You should consult a healthcare professional if you experience:
- Symptoms that persist or worsen over time
- High fever (over 103°F/39.4°C)
- Severe pain or discomfort
- Difficulty breathing
- Unusual or severe symptoms
- Symptoms that interfere with daily activities
- Any concerns about your health

It's always better to be cautious when it comes to your health."""
    
    if "healthy" in user_input and ("lifestyle" in user_input or "living" in user_input):
        return """**Tips for Healthy Living:**

1. **Nutrition:** Eat a balanced diet with plenty of fruits, vegetables, whole grains, and lean proteins
2. **Exercise:** Aim for 150 minutes of moderate activity per week
3. **Sleep:** Get 7-9 hours of quality sleep nightly
4. **Hydration:** Drink plenty of water throughout the day
5. **Stress Management:** Practice relaxation techniques like meditation or yoga
6. **Regular Checkups:** Visit your doctor for preventive care
7. **Avoid Harmful Habits:** Limit alcohol, avoid smoking

Small, consistent changes can make a big difference in your overall health!"""
    
    # Default response
    return """I'm here to help with general health information. I can provide information about:

- Common conditions (fever, cold, cough, headache)
- When to see a doctor
- Healthy lifestyle tips
- General wellness advice

Could you please be more specific about what you'd like to know? Or ask me something like:
- "Tell me about fever"
- "When should I see a doctor?"
- "Tips for healthy living"

**Remember:** For specific medical concerns, always consult a healthcare professional."""

@cl.on_chat_end
async def end():
    """Handle chat end"""
    await cl.Message(content="Thank you for using Healthcare Assistant. Stay healthy! 🌟").send()