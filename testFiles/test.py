import streamlit as st
from google import genai

# Set page config
st.set_page_config(page_title="Language Translator Chatbot", page_icon="🗣️")

# Initialize the client
client = genai.Client(api_key="AIzaSyC7EQbTwnugtG8XpLc-QcvrJ03gEjltE-U")

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Create the Streamlit interface
st.title("Language Assistant Chatbot")

# Add language selection dropdown
languages = [
    "English", "Hindi", "Bengali", "Tamil", "Telugu", 
    "Marathi", "Gujarati", "Urdu", "Kannada", 
    "Malayalam", "Odia", "Punjabi"
]
selected_language = st.selectbox("Select output language:", languages)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Add chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Generate and display assistant response
    prompt = f"{user_input} (reply in {selected_language})"
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    
    with st.chat_message("assistant"):
        st.write(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})

# Add a clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.experimental_rerun()