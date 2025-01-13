# Medical Chatbot with Appointment Booking 🏥

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-latest-red.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-integrated-green.svg)](https://openai.com)
[![LangChain](https://img.shields.io/badge/LangChain-latest-yellow.svg)](https://langchain.org)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

## Overview 🎯

The Medical Chatbot is a Streamlit-powered virtual medical assistant that combines advanced NLP with appointment scheduling capabilities. Using retrieval-augmented generation (RAG) techniques and trusted medical references, it provides accurate medical information while facilitating seamless appointment bookings.

![Medical Chatbot Demo](assets/demo.gif)

## Features ✨

- 🤖 **Intelligent Medical Q&A**
  - RAG-based information retrieval
  - Trusted medical reference integration
  - Context-aware responses

- 💬 **Interactive Interface**
  - User-friendly Streamlit interface
  - Empathetic conversation design
  - Real-time response generation

- 📅 **Appointment Management**
  - Keyword-triggered booking flow
  - Automated scheduling system
  - Confirmation notifications

- 🔒 **Safety & Compliance**
  - Medical disclaimers
  - Educational purpose clarity
  - Professional guidance emphasis

## Technical Architecture 🏗️

```
medical-chatbot/
├── app.py                # Main Streamlit application
├── requirements.txt      # Project dependencies
├── code.py               # Code without GUI
```

## Installation 🚀

### Prerequisites

- Python 3.7+
- OpenAI API key
- Modern web browser

### Setup Steps

1. Clone the repository:
```bash
git clone https://github.com/Siddhant231xyz/Medical-ChatBot.git
cd Medical-ChatBot
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure OpenAI API:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Usage Guide 📚

1. Start the application:
```bash
streamlit run app.py
```

2. Interact with the chatbot:
   - Ask medical questions
   - Type "appointment" for booking
   - Review responses with disclaimers

## How It Works 🔄

1. **Document Processing**
   - PDF text chunking
   - Vector store indexing
   - Semantic search capability

2. **Conversation Flow**
   - Query understanding
   - Context retrieval
   - Response generation
   - Appointment integration

## Deployment Options 🌐

### Streamlit Cloud
1. Connect to GitHub repository
2. Configure environment variables
3. Deploy application

### Alternative Platforms
- Heroku
- AWS
- Google Cloud

## Contributing 🤝

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## Dependencies 📦

- streamlit
- langchain-openai
- langchain-core
- langchain-community
- langchain-text-splitters
- langgraph

## License 📝

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
Created with ❤️ by Medical ChatBot Team
</div>
