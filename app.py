import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from io import BytesIO
import time

# Configure your Gemini API
API_KEY = st.secrets["general"]["api_key"]
genai.configure(api_key=API_KEY)

# Function to get response from Gemini model
def get_gemini_response(conversation_history):
    model = genai.GenerativeModel("gemini-1.5-flash")
    context = "\n".join(conversation_history)
    response = model.generate_content(context)
    return clean_response(response.text)

# Clean Response function
def clean_response(response_text):
    cleaned_text = response_text.replace('*', '').replace('##', '').strip()
    return cleaned_text

# Function to speak the response using gTTS and automatically play
def speak(text):
    tts = gTTS(text, lang='en')
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    st.session_state.audio_bytes = audio_file.read()  # Save audio data in session state

# Function to handle user input submission
def handle_input():
    user_input = st.session_state.user_input
    if user_input:
        # Append user input to conversation history with emoji
        st.session_state.conversation_history.append(f"🙎‍♂️ You: {user_input}")

        # Generate AI response
        response = get_gemini_response(st.session_state.conversation_history)

        # Append AI response to conversation history with emoji
        st.session_state.conversation_history.append(f"🤖 AI: {response}")

        # Clear input box
        st.session_state.user_input = ""

        # Speak the response automatically if read out is activated
        if st.session_state.read_out:
            time.sleep(0.5)  # Adjust the duration as needed
            speak(response)

# Streamlit UI setup
st.title("Real Time Conversational AI with Memory")
st.write("Chat with the AI below!")

# Initialize session states
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "read_out" not in st.session_state:
    st.session_state.read_out = False
if "audio_bytes" not in st.session_state:
    st.session_state.audio_bytes = None

# Display conversation history container
conversation_placeholder = st.container()
with conversation_placeholder:
    for message in st.session_state.conversation_history:
        if message.startswith("🙎‍♂️ You:"):
            st.markdown(
                f'<div style="text-align: right; background-color: #0056b3; color: white; border-radius: 10px; padding: 10px; margin: 5px; max-width: 70%; display: inline-block; box-shadow: 0 0 10px rgba(0,0,0,0.3); margin-left: auto;">{message}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div style="text-align: left; background-color: #007bff; color: white; border-radius: 10px; padding: 10px; margin: 5px; max-width: 70%; display: inline-block; box-shadow: 0 0 10px rgba(0,0,0,0.3);">{message}</div>',
                unsafe_allow_html=True
            )

# Checkbox to select if AI responses should be read aloud
st.session_state.read_out = st.checkbox("Read AI responses aloud")

# User input section at the bottom
input_placeholder = st.text_input(
    "Type your message:",
    value="",
    key="user_input",
    placeholder="Enter your message here...",
    on_change=handle_input
)

# Automatically play audio if it exists in session state
if st.session_state.audio_bytes:
    st.audio(st.session_state.audio_bytes, format="audio/mp3")

# Button to clear conversation history
if st.button("Clear Conversation"):
    st.session_state.conversation_history = []
    st.write("Conversation cleared.")
