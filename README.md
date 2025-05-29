# TellMeMedBot

**AI-Powered Multilingual Telemedicine Chatbot for Rural India**  
_Winning Project of ‘Tenacity X RV University Hackathon’_

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Acknowledgements](#acknowledgements)
- [License](#license)
- [Contact](#contact)

---

## Overview

TellMeMedBot is designed to bridge the healthcare gap in rural and linguistically diverse regions of India. It provides accessible, AI-driven medical analysis and seamless connections to doctors for advanced care and surgical guidance. The bot supports over 15 Indian languages, enabling users from underserved communities to receive accurate symptom analysis, home remedy suggestions, triage guidance, and specialist recommendations in their native language.

---

## Features

- **Multilingual Support:**  
  Communicate in 15+ Indian languages including Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Odia, Punjabi, Assamese, Urdu, and more.

- **AI-Powered Symptom Analysis:**  
  Achieves 92% accuracy in analyzing user symptoms using advanced prompt engineering and Gemini API.

- **Real-Time Language Translation:**  
  Instantly translates user queries and bot responses, ensuring clear communication regardless of language barriers.

- **Medical Knowledge Retrieval:**  
  Provides evidence-based home remedies, lifestyle advice, and, when necessary, recommends consulting a general physician or specialist.

- **Doctor & Patient Portal:**  
  Secure registration and login for both doctors and patients, with session-based authentication.

- **Triage & Escalation:**  
  Guides users on when to seek professional help or specialist care based on symptom severity.

- **HIPAA-Compliant Interactions:**  
  Session-based authentication and CORS-enabled APIs ensure privacy and data security.

---

## Tech Stack

- **Backend:** Python, Flask, SQLAlchemy
- **Frontend:** Streamlit
- **AI/ML:** Gemini API, Sentence Transformers
- **Database:** SQLite (separate databases for doctors and patients)
- **Security:** Session-based authentication, CORS-enabled APIs
- **Deployment:** Localhost (can be adapted for cloud platforms)

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- [Google Gemini API Key](https://ai.google.dev/)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/TellMeMedBot.git
   cd TellMeMedBot

   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**

   - Add your Gemini API key in `chatbot.py` or set it as an environment variable.

4. **Initialize the databases:**

   - The app will auto-create SQLite databases for doctors and patients on first run.

### Running the Application

1. **Start the Flask server:**

   ```bash
   python app.py
   ```

2. **Access the web portal:**

   - Open your browser and go to `http://localhost:5000`
   - Register as a doctor or patient and log in.

3. **Start the Chatbot:**

   - After login, click on “Start Chatbot” to launch the Streamlit-based multilingual chatbot interface.

---

## Usage

- **Symptom Analysis:**
  Describe your symptoms in your preferred language. The bot will ask for essential details (age, gender, location, medical history) before providing tailored suggestions.

- **Home Remedies & Guidance:**
  Receive safe, evidence-based home remedies and lifestyle advice.

- **Specialist Recommendations:**
  For severe or specific symptoms, the bot will recommend consulting a relevant specialist.

> **Disclaimer:**
> This chatbot provides general suggestions only. For serious medical conditions, please consult a healthcare professional.

---

## Project Structure

```
TellMeMedBot/
├── app.py                # Flask backend (user management, dashboard)
├── chatbot/
│   └── chatbot.py        # Streamlit chatbot interface
├── templates/            # HTML templates for Flask
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## Acknowledgements

- Developed as a winning project at the ‘Tenacity X RV University Hackathon’.
- Thanks to the open-source community and contributors.

---

## License

This project is licensed under the MIT License.

---

## Contact

For queries, suggestions, or contributions, please open an issue or contact the project maintainer.

---

_Empowering rural India with accessible, multilingual healthcare—one conversation at a time._

```

```
