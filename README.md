# Medical Chatbot with Appointment Booking

Welcome to the **Medical Chatbot with Appointment Booking** project! This interactive, Streamlit-powered application serves as a cutting-edge virtual medical assistant. It leverages state-of-the-art language models alongside retrieval-augmented generation (RAG) techniques to answer users' medical questions using a trusted medical reference and, when needed, smoothly guides users through an appointment booking process.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

This project integrates advanced Natural Language Processing (NLP) with a simple appointment scheduling flow. The Medical Chatbot reads a trusted medical reference (a PDF book), splits it into manageable chunks, and indexes the knowledge using vector stores. When users ask a question, the chatbot retrieves the most relevant information and generates a concise, empathetic, and disclaimer-included answer.

The appointment booking module adds another layer of interactivity by allowing users to seamlessly transition from asking questions to scheduling appointments—all within one intuitive interface.

## Features

- **Dynamic Medical Q&A:**  
  Uses retrieval-augmented generation (RAG) to provide answers based on the most relevant information from a medical reference PDF.
  
- **Empathetic Chat Interface:**  
  Built on Streamlit, the chatbot offers a user-friendly web interface designed to engage and inform users.
  
- **Appointment Booking Integration:**  
  Easily switch to an appointment booking flow by typing keywords like "appointment" or "book". Users can then provide their details and receive a simulated appointment confirmation.
  
- **Cutting-Edge Technology:**  
  Powered by models from OpenAI and integrated with LangChain, this application represents a modern approach to conversational AI in the healthcare domain.
  
- **Clear Medical Disclaimers:**  
  All responses include a disclaimer, ensuring users understand that the information provided is solely for educational purposes and not a substitute for professional medical advice.

## How It Works

1. **Document Preparation & Indexing:**  
   The medical reference PDF is loaded and segmented into overlapping text chunks using a recursive splitter. These chunks are then indexed in an in-memory vector store, enabling fast and relevant retrieval based on user queries.

2. **Retrieval-Augmented Generation:**  
   When a user asks a question, the application searches for the most relevant chunks of text in the vector store. The content is then combined with a set of carefully crafted medical instructions (which include empathy, conciseness, and a disclaimer) to generate a precise response.

3. **Appointment Booking Flow:**  
   If a user expresses intent to book an appointment (detected via keywords), the chatbot shifts the conversation to gather the necessary appointment details, simulating a seamless booking process.

4. **Streamlit Interface:**  
   The entire interaction is handled via a Streamlit web app, making the experience interactive, real-time, and easily accessible through a web browser.

## Installation

To get a local copy up and running, follow these simple steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/<your-username>/<repo-name>.git
   cd <repo-name>
Create a Virtual Environment (recommended):

bash
Copy code
python -m venv venv
# Activate the environment:
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
The requirements.txt includes:

streamlit
langchain-openai
langchain-core
langchain-community
langchain-text-splitters
langgraph
Set Up Your OpenAI API Key:

Ensure your OpenAI API key is set in your environment. You can do this directly or use getpass as prompted in the application.

Usage
Run the Streamlit app using the following command:

bash
Copy code
streamlit run app.py
Open the provided URL (e.g., http://localhost:8501) in your web browser to start interacting with the Medical Chatbot. Ask any medical-related questions or type "appointment" to switch to the appointment booking flow.

Deployment
This project is ready for deployment on platforms such as Streamlit Community Cloud:

Push your code to GitHub.
Navigate to Streamlit Community Cloud and link your GitHub repository.
Set app.py as the main file and deploy.
Follow similar steps for other cloud providers if desired.

Contributing
Contributions are welcome! If you have suggestions or improvements, please feel free to open an issue or submit a pull request. For major changes, please open an issue first to discuss what you would like to change.
