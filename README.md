# Real-Time Conversational AI with Memory

This Streamlit application enables real-time interaction with an AI conversational model that remembers past exchanges within each session. The app integrates Google’s Gemini model for generating responses and gTTS (Google Text-to-Speech) for converting text into speech, providing an engaging and interactive experience. Although the app stores audio bytes for AI responses, users must manually play the audio if they wish to hear the AI's response aloud.

## Features

- **Conversational Memory**: The app retains conversation history throughout each session, enabling it to respond in context based on prior messages. This memory is cleared when starting a new session or clicking the "Clear Conversation" button.
- **Text-to-Speech Support**: Using gTTS, AI responses are saved as audio files, which users can play manually if the "Read AI responses aloud" option is selected.
- **Dynamic Chat Interface**: A user-friendly interface displays chat history, with user messages appearing on the right and AI responses on the left for easy reading.
- **Manual Audio Playback**: When the "Read AI responses aloud" option is selected, an audio player appears alongside the AI response, allowing users to listen to the response by pressing play.
