# utils/chatbot.py
import os
from groq import Groq
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

def get_response(user_msg):
    """
    Sends user message to Groq model and returns CCI-specific response.
    """
    # System instruction to restrict answers
    system_prompt = (
        "You are an expert in mobile communications. "
        "Answer only questions related to co-channel interference, mobile communication "
        "cluster size (N), interfering cells (i0), or S/I formula. "
        "If question is unrelated, reply: 'I can only answer CCI-related questions.'"
    )

    # Prepare conversation messages
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_msg}
    ]

    # Create completion
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        temperature=0.5,  # less randomness
        max_completion_tokens=500,
        top_p=1,
        reasoning_effort="medium",
        stream=False  # set False to get full response at once
    )

    # Extract the model's reply
    reply = completion.choices[0].message.content.strip()
    return reply