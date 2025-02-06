import streamlit as st
from google import genai
import time

# Initialize Gemini client
client = genai.Client(api_key="AIzaSyC7EQbTwnugtG8XpLc-QcvrJ03gEjltE-U")

# Set page config for better appearance
st.set_page_config(page_title="Home Remedies Chatbot", page_icon="🌿", layout="wide")

# Custom CSS for smoother animations
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        transition: all 0.3s ease-in-out;
    }
    .stMarkdown {
        transition: opacity 0.5s ease-in-out;
    }
    </style>
    """, unsafe_allow_html=True)

# Set up Streamlit interface with animation
with st.container():
    st.title("🌿 Home Remedies Chatbot")
    st.write("Describe your symptoms and get natural remedy suggestions")

# Language selection with improved UI
languages = ["English", "Hindi", "Bengali", "Tamil", "Telugu", 
            "Marathi", "Gujarati", "Urdu", "Kannada", 
            "Malayalam", "Odia", "Punjabi","Assamese"]
selected_language = st.sidebar.selectbox("🌍 Select Language", languages)

# Initialize chat session
if 'chat' not in st.session_state:
    st.session_state.chat = client.chats.create(model="gemini-2.0-flash")
    
# Initialize message history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat history with smooth transitions
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"])

# Chat input with improved response handling
if prompt := st.chat_input("What symptoms are you experiencing? 🤔"):
    # Add user message to chat
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get AI response with smooth typing animation
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Check if it's a greeting
        greetings = ["hi", "hello", "hey", "greetings", "namaste"]
        if prompt.lower() in greetings:
            context = f"Respond with a friendly greeting in {selected_language} and ask about the symptoms."
        else:
            context = f"As a medical advisor, suggest natural home remedies for the following symptoms: {prompt}. Only suggest safe, common household remedies and include any necessary precautions. Please provide the response in {selected_language} language."
        
        # Improved streaming animation
        response = st.session_state.chat.send_message_stream(context)
        for chunk in response:
            full_response += chunk.text
            # Add a small delay for smoother typing effect
            time.sleep(0.01)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Add a styled disclaimer
with st.sidebar.container():
    st.markdown("---")
    st.warning("⚠️ **Disclaimer:** This chatbot provides general suggestions only. For serious medical conditions, please consult a healthcare professional.")