# Medical Chatbot with Appointment Booking 🏥

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-latest-red.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-integrated-green.svg)](https://openai.com)
[![LangChain](https://img.shields.io/badge/LangChain-latest-yellow.svg)](https://langchain.org)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

## Overview 🎯

The Medical Chatbot is a Streamlit-powered virtual medical assistant that combines advanced NLP with appointment scheduling capabilities. Using retrieval-augmented generation (RAG) techniques and trusted medical references, it provides accurate, empathetic medical information while enabling patients to book appointments directly. Appointment data is stored in an AWS RDS database.

![Medical Chatbot Demo](assets/demo.gif)

## Features ✨

- 🤖 **Intelligent Medical Q&A**
  - RAG-based information retrieval from a medical book PDF
  - Empathetic and reassuring responses
  - Suggestions to book an appointment if symptoms are severe

- 💬 **Interactive Interface**
  - User-friendly Streamlit interface
  - Context-aware and friendly conversation design

- 📅 **Appointment Management**
  - Easy-to-use appointment booking form
  - Appointment details stored directly into an AWS RDS database
  - Option to view booked appointments directly in the app

- 🔒 **Safety & Compliance**
  - Medical disclaimers
  - Emphasis on educational and supportive guidance

## Technical Architecture 🏗️

```
medical-chatbot/
├── app.py                 # Main Streamlit application with medical Q&A & appointment booking
├── requirements.txt       # Project dependencies
├── Dockerfile             # Containerization instructions
├── .dockerignore          # Files to ignore when building the Docker image
├── .streamlit/secrets.toml           # Secrets file (contains DATABASE_URL, etc.)
├── app_local.py           # Streamlit app for localhost
```

### How It Works

1. **Document Processing**
   - A medical book PDF is uploaded and processed by splitting its text into chunks.
   - LangChain is used to create embeddings and retrieve context for answering user queries.

2. **Conversation Flow**
   - The user asks medical questions.
   - The chatbot responds in a friendly, compassionate manner and suggests booking an appointment if symptoms seem severe.

3. **Appointment Booking**
   - Users can book an appointment by filling out a form.
   - Appointment details are inserted directly into an AWS RDS database using SQLAlchemy.

4. **Viewing Appointments**
   - A separate section in the app displays the list of booked appointments.

## Installation 🚀

### Prerequisites

- Python 3.7+
- Docker (for containerization)
- Git
- An OpenAI API key
- AWS RDS (MySQL/PostgreSQL) instance for storing appointments

### Setup Steps

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/Siddhant231xyz/Medical-ChatBot.git
    cd Medical-ChatBot
    ```

2. **Create a Virtual Environment (for local development):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Secrets:**

   Create a directory named `.streamlit` in the project root and add a `secrets.toml` file:
   
    ```toml
    # .streamlit/secrets.toml
    DATABASE_URL = "postgresql://username:password@your-rds-endpoint:port/dbname"
    OPENAI_API_KEY = "your-api-key-here"
    ```

   *Note:* Ensure the connection string is wrapped in quotes.

## Usage Guide 📚

1. **Start the Application:**

    ```bash
    streamlit run app.py
    ```

2. **Interact with the Chatbot:**
   - Upload a medical book PDF.
   - Ask medical questions to receive friendly, empathetic responses.
   - Use the appointment booking form to schedule an appointment.
   - View the list of booked appointments in the "View Appointments" section.

## Deployment Options 🌐

### Docker Deployment

This application is containerized using Docker. Follow these steps:

1. **Dockerfile:**

    The provided `Dockerfile` contains:

    ```dockerfile
    FROM python:3.9-slim

    ENV PYTHONDONTWRITEBYTECODE=1
    ENV PYTHONUNBUFFERED=1
    ENV OPENAI_API_KEY="<api_key>"

    WORKDIR /app

    # Copy and install dependencies
    COPY requirements.txt /app/
    RUN pip install --upgrade pip && pip install -r requirements.txt

    # Copy application code and secrets
    COPY app.py /app/
    COPY .streamlit /app/.streamlit

    # Expose Streamlit's default port
    EXPOSE 8501

    # Run the Streamlit app
    CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
    ```

2. **.dockerignore File:**

    ```plaintext
    __pycache__/
    *.pyc
    venv/
    ```

3. **Build the Docker Image:**

    ```bash
    docker build -t medical-chatbot .
    ```

4. **Run the Docker Container:**

    ```bash
    docker run -d -p 8501:8501 medical-chatbot
    ```

### AWS EC2 Deployment

1. **Launch an EC2 Instance:**
   - Use an Amazon Linux 2 (or similar) instance.
   - Attach an IAM role with appropriate permissions if needed.
   
2. **Install Docker on the EC2 Instance:**

    ```bash
    sudo yum update -y
    sudo amazon-linux-extras install docker -y
    sudo service docker start
    sudo usermod -a -G docker ec2-user
    ```

3. **Deploy Your Container:**
   - Copy your project to the EC2 instance (e.g., via Git or SCP).
   - Build and run your Docker container using the commands above.

### AWS RDS Setup (MySQL/PostgreSQL)

1. **Create an RDS Instance:**
   - Log in to the AWS Console → RDS → Create database.
   - Choose MySQL or PostgreSQL.
   - Configure the instance and note the endpoint, port, username, and password.

2. **Create the Appointments Table:**

   For **PostgreSQL**:
   ```sql
   CREATE TABLE appointments (
       id SERIAL PRIMARY KEY,
       name VARCHAR(255) NOT NULL,
       email VARCHAR(255) NOT NULL,
       phone VARCHAR(50) NOT NULL,
       appointment_datetime TIMESTAMP NOT NULL,
       symptoms TEXT,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

   For **MySQL**:
   ```sql
   CREATE TABLE appointments (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255) NOT NULL,
       email VARCHAR(255) NOT NULL,
       phone VARCHAR(50) NOT NULL,
       appointment_datetime DATETIME NOT NULL,
       symptoms TEXT,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

3. **Configure the DATABASE_URL:**
   Update your `.streamlit/secrets.toml` file with the connection string, e.g.,
   ```toml
   DATABASE_URL = "postgresql://username:password@your-rds-endpoint:port/dbname"
   ```

## Detailed Steps & Commands

### Docker:
- Build: `docker build -t medical-chatbot .`
- Run: `docker run -d -p 8501:8501 medical-chatbot`

### EC2 Setup:
- Update and install Docker:
  ```bash
  sudo yum update -y
  sudo amazon-linux-extras install docker -y
  sudo service docker start
  sudo usermod -a -G docker ec2-user
  ```
- Deploy your container on EC2 using the Docker commands above.

### RDS Setup:
- Create an RDS instance in the AWS Console.
- Connect with a database client (like pgAdmin, MySQL Workbench, or CLI tools) and create the appointments table using the provided SQL.

### Secrets & Environment:
- Create a `.streamlit/secrets.toml` file with your DATABASE_URL and OPENAI_API_KEY.
- Ensure the secrets file is copied into the Docker container (see Dockerfile).

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
- sqlalchemy
- requests
- numpy
- (and other dependencies as listed in requirements.txt)

## License 📝

This project is licensed under the MIT License - see the LICENSE file for details.

<div align="center"> Created with ❤️ by the Medical ChatBot Team </div>
