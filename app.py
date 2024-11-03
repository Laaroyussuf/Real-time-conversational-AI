import streamlit as st
import google.generativeai as genai
import pyttsx3
import time

# Configure your Gemini API
API_KEY = st.secrets["general"]["api_key"]
genai.configure(api_key=API_KEY)

# Function to get response from Gemini model
def get_gemini_response(conversation_history):
    model = genai.GenerativeModel("gemini-1.5-flash")
    context = "\n".join(conversation_history)
    
    try:
        response = model.generate_content(context)
        # Ensure response exists and has a 'text' attribute
        if hasattr(response, 'text'):
            return clean_response(response.text)
        else:
            st.error("AI response is empty or unexpected format.")
            return "I'm sorry, I couldn't generate a response at this time."
    except Exception as e:
        st.error(f"Error generating AI response: {e}")
        return "An error occurred while generating the response."

# Clean Response function
def clean_response(response_text):
    return response_text.replace('*', '').replace('##', '').strip()

# Function to speak the response if 'read_out' is selected
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Handle user input submission
def handle_input():
    user_input = st.session_state.user_input
    if user_input:
        st.session_state.conversation_history.append(f"🙎‍♂️ You: {user_input}")
        response = get_gemini_response(st.session_state.conversation_history)
        st.session_state.conversation_history.append(f"🤖 AI: {response}")
        st.session_state.user_input = ""

        # Automatically speak response if 'read_out' is enabled
        if st.session_state.read_out:
            time.sleep(0.5)
            speak(response)

# Streamlit UI setup
st.title("Real-Time Conversational AI with Memory")
st.write("Chat with the AI below!")

# Initialize conversation history and read out option
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "read_out" not in st.session_state:
    st.session_state.read_out = False

# Conversation history display
conversation_placeholder = st.container()
with conversation_placeholder:
    for message in st.session_state.conversation_history:
        alignment = "right" if message.startswith("🙎‍♂️ You:") else "left"
        color = "#0056b3" if alignment == "right" else "#007bff"
        st.markdown(
            f'<div style="text-align: {alignment}; background-color: {color}; color: white; '
            f'border-radius: 10px; padding: 10px; margin: 5px; max-width: 70%; display: inline-block;'
            ' box-shadow: 0 0 10px rgba(0,0,0,0.3);">{message}</div>',
            unsafe_allow_html=True
        )

# Checkbox for read aloud option
st.session_state.read_out = st.checkbox("Read AI responses aloud")

# Input section with Enter key submission
st.text_input(
    "Type your message:",
    value="",
    key="user_input",
    placeholder="Enter your message here...",
    on_change=handle_input
)

# Button to clear conversation history
if st.button("Clear Conversation"):
    st.session_state.conversation_history = []
    st.write("Conversation cleared.")
