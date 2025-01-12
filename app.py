import getpass
import os
import streamlit as st

# Ensure the OpenAI API key is set
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

# ---------------------------
# LLM, Embeddings, Vector Store, and Document Loading Setup
# ---------------------------
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
llm = ChatOpenAI(model="gpt-4o-mini")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

from langchain_core.vectorstores import InMemoryVectorStore
vector_store = InMemoryVectorStore(embeddings)

# Load the medical reference book PDF
from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader("C:/Users/admin/Desktop/010041093.pdf")

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load and split the PDF into chunks
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
all_splits = text_splitter.split_documents(docs)

# Index the document chunks into the vector store
_ = vector_store.add_documents(documents=all_splits)

# ---------------------------
# Define Medical Instructions and LangGraph Pipeline
# ---------------------------
medical_instructions = (
    "You are a helpful, knowledgeable, and empathetic medical chatbot. "
    "Your responses are based on reliable medical references provided in the context. "
    "Include the following disclaimer in your responses: 'This information is for educational purposes only and is not a substitute for professional medical advice.' "
    "Keep your answer concise (maximum three sentences) and do not provide a definitive diagnosis. "
    "If you are unsure, say that you do not have enough information."
)

from langgraph.graph import START, StateGraph
from typing_extensions import TypedDict, List

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

def retrieve(state: State) -> State:
    """Retrieve the most relevant document chunks from the medical reference."""
    # Retrieve top 2 most relevant chunks based on the question.
    retrieved_docs = vector_store.similarity_search(state["question"], k=2)
    return {"question": state["question"], "context": retrieved_docs}

def generate(state: State) -> State:
    """Generate an answer based on the retrieved context and medical instructions."""
    # Combine the content from the retrieved documents.
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    
    # Build messages: a system message including instructions and context, and a user message.
    messages = [
        {"role": "system", "content": f"{medical_instructions}\n\nContext:\n{docs_content}"},
        {"role": "user", "content": state["question"]}
    ]
    
    # Invoke the LLM to generate an answer.
    response = llm.invoke(messages)
    return {"question": state["question"], "context": state["context"], "answer": response.content}

# Build the medical question-answering chain using LangGraph.
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
medical_graph = graph_builder.compile()

# ---------------------------
# Define the Appointment Booking Flow
# ---------------------------
def appointment_booking_flow(user_question: str, appointment_details: str) -> State:
    """
    A simple appointment booking flow.
    Here we simulate a booking confirmation using the provided appointment details.
    """
    confirmation = (
        f"Your appointment has been booked for {appointment_details}. "
        "Please check your email for confirmation details. "
        "Note: This information is for educational purposes and does not confirm an actual booking."
    )
    return {"question": user_question, "context": [], "answer": confirmation}

# ---------------------------
# Streamlit App: Chat Interface
# ---------------------------
st.title("Medical Chatbot with Appointment Booking")
st.write("Ask your medical questions or type 'appointment' to book an appointment.")

# Use Streamlit's session_state to store conversation history and appointment mode.
if "messages" not in st.session_state:
    st.session_state.messages = []  # store tuples (user_message, bot_answer)
if "appointment_mode" not in st.session_state:
    st.session_state.appointment_mode = False

# Define a container for chat and (if needed) for appointment details.
chat_container = st.container()
with chat_container:
    # Display conversation history.
    for i, (user_msg, bot_msg) in enumerate(st.session_state.messages):
        st.markdown(f"**You:** {user_msg}")
        st.markdown(f"**Chatbot:** {bot_msg}")

# Input for new message.
user_input = st.text_input("Your message:", key="user_input")

if st.button("Send") and user_input:
    # Check if the message is meant for appointment booking.
    if "appointment" in user_input.lower() or "book" in user_input.lower():
        st.session_state.appointment_mode = True
        st.session_state.user_question = user_input
        st.experimental_rerun()  # Rerun to show appointment details input.
    else:
        # Run the medical RAG pipeline.
        state_in = {"question": user_input, "context": []}
        result = medical_graph.invoke(state_in)
        st.session_state.messages.append((user_input, result["answer"]))
        st.experimental_rerun()

# If appointment mode is active, show additional input for appointment details.
if st.session_state.appointment_mode:
    st.info("Appointment Booking Mode: Please enter your preferred appointment details below.")
    appointment_details = st.text_input("Appointment Details (e.g., date, time, notes):", key="appointment_details")
    if st.button("Confirm Appointment"):
        result = appointment_booking_flow(st.session_state.user_question, appointment_details)
        st.session_state.messages.append((st.session_state.user_question, result["answer"]))
        st.session_state.appointment_mode = False  # Reset mode after booking
        st.experimental_rerun()

# A button to clear the conversation.
if st.button("Clear Conversation"):
    st.session_state.messages = []
    st.session_state.appointment_mode = False
    st.experimental_rerun()
