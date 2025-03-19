import os
import tempfile
import json
import streamlit as st
import pandas as pd
import requests
import numpy as np
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import HumanMessage
from sqlalchemy import create_engine, text

# =============================================================================
# Helper Functions
# =============================================================================

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)

def load_and_process_pdf(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    return splits

def query_medical_book(question: str, docs):
    """Combine the content from the most relevant docs and query the LLM with friendly, supportive instructions."""
    # Compute the query embedding.
    query_embedding = st.session_state.embeddings.embed_query(question)
    
    # For each document chunk, compute its embedding and similarity to the query.
    doc_similarities = []
    for doc in docs:
        doc_embedding = st.session_state.embeddings.embed_query(doc.page_content)
        sim = cosine_similarity(query_embedding, doc_embedding)
        doc_similarities.append((doc, sim))
    
    # Sort the documents by similarity score (descending order).
    doc_similarities.sort(key=lambda x: x[1], reverse=True)
    # Select the top 3 most relevant chunks.
    top_docs = [doc for doc, sim in doc_similarities[:3]]
    
    # Combine excerpts from the selected document chunks.
    context = "\n\n".join(doc.page_content for doc in top_docs)
    
    # System instructions for the LLM:
    system_instructions = (
        "You are a compassionate and friendly medical assistant. "
        "Your responses should be written in a gentle and reassuring tone, avoiding any technical or frightening language. "
        "If the patient's symptoms appear severe or concerning, kindly suggest booking an appointment. "
        "Only answer queries related to medical issues."
    )
    
    # Build the full prompt.
    prompt = (
        f"{system_instructions}\n\n"
        f"Medical Book Excerpt:\n{context}\n\n"
        f"Patient Question: {question}\n\n"
        "Answer:"
    )
    
    llm = st.session_state.llm
    # Wrap the prompt in a HumanMessage and send it to the LLM.
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content

def book_appointment(name, email, phone, appointment_datetime, symptoms):
    """Insert appointment details directly into the AWS RDS database using SQLAlchemy."""
    DATABASE_URL = st.secrets["DATABASE_URL"]
    engine = create_engine(DATABASE_URL)
    try:
        with engine.connect() as conn:
            insert_query = text("""
                INSERT INTO appointments (name, email, phone, appointment_datetime, symptoms)
                VALUES (:name, :email, :phone, :appointment_datetime, :symptoms)
            """)
            conn.execute(insert_query, {
                "name": name,
                "email": email,
                "phone": phone,
                "appointment_datetime": appointment_datetime,
                "symptoms": symptoms
            })
            conn.commit()
        return True, "Appointment booked successfully!"
    except Exception as e:
        return False, str(e)

def get_appointments():
    DATABASE_URL = st.secrets.get("DATABASE_URL") or os.environ.get("DATABASE_URL")
    engine = create_engine(DATABASE_URL)
    try:
        with engine.connect() as conn:
            query = text("SELECT id, name, email, phone, appointment_datetime, symptoms, created_at FROM appointments ORDER BY created_at DESC")
            result = conn.execute(query)
            appointments = result.fetchall()
        df = pd.DataFrame(appointments, columns=["ID", "Name", "Email", "Phone", "Appointment DateTime", "Symptoms", "Created At"])
        return df
    except Exception as e:
        st.error(f"Error retrieving appointments: {e}")
        return None

# =============================================================================
# Session State Initialization
# =============================================================================

if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.write("Initializing… please wait (this may take a minute).")
    
    # --- Initialize LLM and Embeddings ---
    st.session_state.llm = ChatOpenAI(model="gpt-4o-mini")
    st.session_state.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    
    st.success("Initialization complete!")

# =============================================================================
# Streamlit UI
# =============================================================================

st.title("MedicalBook Analyzer & Appointment Booking System")

tabs = st.tabs(["Medical Q&A", "Book Appointment", "View Appointments"])

# --- Medical Q&A Tab ---
with tabs[0]:
    st.header("Medical Q&A")
    uploaded_medbook = st.file_uploader("Upload a Medical Book (PDF)", type=["pdf"])
    if uploaded_medbook is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_medbook.read())
            tmp_file_path = tmp_file.name
        medbook_docs = load_and_process_pdf(tmp_file_path)
        st.success("Medical book processed successfully!")
    
        question = st.text_input("Ask a question about patient symptoms or possible diseases:")
        if st.button("Submit Question"):
            if not question:
                st.warning("Please enter a question.")
            else:
                answer = query_medical_book(question, medbook_docs)
                st.markdown("### Answer")
                st.write(answer)
    else:
        st.info("Please upload a Medical Book PDF to begin.")

# --- Appointment Booking Tab ---
with tabs[1]:
    st.header("Book an Appointment")
    with st.form("appointment_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        appointment_datetime = st.text_input("Preferred Appointment Date & Time (YYYY-MM-DD HH:MM)")
        symptoms = st.text_area("Describe your symptoms")
        submitted = st.form_submit_button("Book Appointment")
    
    if submitted:
        if not (name and email and phone and appointment_datetime and symptoms):
            st.warning("Please fill out all fields.")
        else:
            success, result = book_appointment(name, email, phone, appointment_datetime, symptoms)
            if success:
                st.success(result)
            else:
                st.error(f"Failed to book appointment: {result}")

# --- View Appointments Tab ---
with tabs[2]:
    st.header("View Appointments")
    df = get_appointments()
    if df is not None and not df.empty:
        st.dataframe(df)
    else:
        st.info("No appointments found.")
