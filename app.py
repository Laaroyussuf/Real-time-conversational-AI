import streamlit as st
import google.generativeai as genai
import requests
import time
import re

# Configure your Gemini API
API_KEY = st.secrets["general"]["api_key"]
genai.configure(api_key=API_KEY)

# Replace with your actual D-ID API key
DID_API_KEY = st.secrets["general"]["did_api_key"]

# Function to get response from Gemini model
def get_gemini_response(conversation_history):
    model = genai.GenerativeModel("gemini-1.5-flash")
    context = "\n".join(conversation_history)
    response = model.generate_content(context)
    return clean_response(response.text)

# Clean Response function
def clean_response(response_text):
    # Remove emojis and special characters
    cleaned_text = re.sub(r'[^\w\s,.-]', '', response_text).strip()
    return cleaned_text

# Function to generate avatar video using D-ID API
def generate_avatar_video(input_text, source_url):
    url = "https://api.d-id.com/clips"
    headers = {
        "Authorization": f"Basic {DID_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "source_url": source_url,
        "script": {
            "type": "text",
            "subtitles": "false",
            "provider": {
                "type": "microsoft",
                "voice_id": "Sara"
            },
            "input": input_text
        },
        "config": {
            "fluent": "false",
            "pad_audio": "0.0"
        }
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        clip_id = response_json["id"]
        video_url = check_video_status(clip_id)
        return video_url if video_url else None
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return None

# Function to check the video status with a shorter interval
def check_video_status(clip_id):
    url = f"https://api.d-id.com/clips/{clip_id}"
    headers = {
        "Authorization": f"Basic {DID_API_KEY}",
        "Content-Type": "application/json"
    }
    while True:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        status_info = response.json()
        if status_info["status"] == "done" and "result_url" in status_info:
            return status_info["result_url"]
        time.sleep(5)

# Function to handle user input submission
def handle_input():
    user_input = st.session_state.user_input
    if user_input:
        st.session_state.conversation_history.append(f"You: {user_input}")
        response = get_gemini_response(st.session_state.conversation_history)
        st.session_state.user_input = ""
        avatar_input_text = response.strip()
        source_url = "https://d-id-public-bucket.s3.us-west-2.amazonaws.com/alice.jpg"
        video_url = generate_avatar_video(avatar_input_text, source_url)
        if video_url:
            st.session_state.video_url = video_url

# Streamlit UI setup
st.title("Real-Time Conversational AI with Avatar Response")
st.write("Chat with Vastlean-AI below!")

# Initialize session states
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "video_url" not in st.session_state:
    st.session_state.video_url = None

# User input section
input_placeholder = st.text_input(
    "Type your message:",
    value="",
    key="user_input",
    placeholder="Chat with Vastlearn-AI...",
    on_change=handle_input
)

# Display the conversation history with only user input in a chat box style
conversation_placeholder = st.container()
with conversation_placeholder:
    for message in st.session_state.conversation_history:
        st.markdown(
            f'<div style="text-align: right; background-color: #0056b3; color: white; border-radius: 10px; padding: 10px; margin: 5px; max-width: 70%; display: inline-block; box-shadow: 0 0 10px rgba(0,0,0,0.3); margin-left: auto;">{message}</div>',
            unsafe_allow_html=True
        )

# Display the generated avatar video under the input box
if st.session_state.video_url:
    st.video(st.session_state.video_url)
