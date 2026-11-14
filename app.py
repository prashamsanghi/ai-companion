import json
import os
import streamlit as st
from openai import OpenAI  # Or use the official Google GenAI SDK

# 1. Setup the Client and System Rulebook
# (Replace with your actual API key or store it securely in environment variables)
client = OpenAI(api_key=os.environ.get("API_KEY"))

SYSTEM_PROMPT = """
You are a personal companion, confidant, and smart co-pilot.
- Speak naturally and conversationally. Avoid robotic assistant talk.
- Hold your ground with anchored conviction (anti-sycophancy) if the user ignores red flags.
- Act as a smart co-pilot: help with school research and drafting, but keep the user in the driver's seat so their brain doesn't get rusty.
"""

# 2. Simple Local Memory File (Your "Memory Bank")
MEMORY_FILE = "companion_memory.json"


def load_memory():
  if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
      return json.load(f)
  return []


def save_memory(messages):
  with open(MEMORY_FILE, "w") as f:
    json.dump(messages, f, indent=2)


# 3. Streamlit Interface Layout
st.title("My AI Companion")
st.write(
    "Your private, evolving space for conversation, brainstorming, and growth."
)

# Initialize chat history from local storage
if "messages" not in st.session_state:
  st.session_state.messages = load_memory()

# Display past messages on app reload
for message in st.session_state.messages:
  if message["role"] != "system":
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

# 4. Handle User Input & API Call
if prompt := st.chat_input("What's on your mind?"):
  # Display user message
  with st.chat_message("user"):
    st.markdown(prompt)
  st.session_state.messages.append({"role": "user", "content": prompt})

  # Prepare full conversation history including the System Prompt
  full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages

  # Call the API
  response = client.chat.completions.create(
      model="gpt-4o-mini",  # Or your preferred model / Gemini API endpoint
      messages=full_messages,
  )

  assistant_reply = response.choices[0].message.content

  # Display assistant response
  with st.chat_message("assistant"):
    st.markdown(assistant_reply)

  st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

  # Save updated history to local memory file
  save_memory(st.session_state.messages)
