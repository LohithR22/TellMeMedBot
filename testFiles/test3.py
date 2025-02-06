import streamlit as st
from google import genai
import time
import requests
import json

# Initialize Gemini client
client = genai.Client(api_key="AIzaSyC7EQbTwnugtG8XpLc-QcvrJ03gEjltE-U")

# Reverie API configuration
REV_API_URL = "https://revapi.reverieinc.com/"
REV_HEADERS = {
    "Content-Type": "application/json",
    "REV-API-KEY": "cb110c58aac13b4afef4fec600ac5da0e382dc37",
    "REV-APP-ID": "com.lohithrgowda22",
    "domain": "generic",
    "REV-APPNAME": "localization",
    "REV-APPVERSION": "3.0"
}

# Language codes mapping
LANGUAGE_CODES = {
    "English": "en",
    "Hindi": "hi",
    "Assamese": "as",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Odia": "or",
    "Punjabi": "pa",
    "Tamil": "ta",
    "Telugu": "te",
    "Urdu": "ur"
}

def translate_text(text, target_lang):
    if target_lang == "en":  # No translation needed for English
        return text
        
    headers = REV_HEADERS.copy()
    headers["src_lang"] = "en"
    headers["tgt_lang"] = target_lang

    payload = {
        "data": [text],
        "enableNmt": True,
        "enableLookup": True
    }

    try:
        response = requests.post(REV_API_URL, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            result = response.json()
            translated_text = result["responseList"][0]["outString"]
            # Format the translated text
            formatted_text = f"**Translated Response:**\n\n{translated_text}"
            return formatted_text
        return text  # Return original text if translation fails
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return text


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


# Modified chat handling
if prompt := st.chat_input("What symptoms are you experiencing? 🤔"):
    # Add user message to chat
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get AI response in English first
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Check if it's a greeting
        greetings = ["hi", "hello", "hey", "greetings", "namaste"]
        if prompt.lower() in greetings:
            context = "Respond with a friendly greeting and ask about the symptoms."
        else:
            context = f"As a medical advisor, suggest natural home remedies for the following symptoms: {prompt}. Only suggest safe, common household remedies and include any necessary precautions."
        # Get English response from Gemini
        response = st.session_state.chat.send_message_stream(context)
        for chunk in response:
            full_response += chunk.text
            time.sleep(0.01)
            message_placeholder.markdown(full_response + "▌")

        # Translate the response if not English
        if selected_language != "English":
            translated_response = translate_text(full_response, LANGUAGE_CODES[selected_language])
            message_placeholder.markdown(translated_response)
            st.session_state.messages.append({"role": "assistant", "content": translated_response})
        else:
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# Rest of your code remains the same...