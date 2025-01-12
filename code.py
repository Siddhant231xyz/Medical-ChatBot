import getpass
import os

# Ensure the OpenAI API key is set
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

# Set up the Chat LLM (using your desired model)
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini")

# Set up embeddings
from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# Create an in-memory vector store to index documents
from langchain_core.vectorstores import InMemoryVectorStore
vector_store = InMemoryVectorStore(embeddings)

# Load the medical reference book PDF
from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader("C:/Users/admin/Desktop/010041093.pdf")

# Document handling utilities
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load and split the PDF into chunks
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
all_splits = text_splitter.split_documents(docs)

# Index the document chunks into the vector store
_ = vector_store.add_documents(documents=all_splits)

# Define specialized medical instructions for the chatbot, including a disclaimer.
medical_instructions = (
    "You are a helpful, knowledgeable, and empathetic medical chatbot. "
    "Your responses are based on reliable medical references provided in the context. "
    "Include the following disclaimer in your responses: 'This information is for educational purposes only and is not a substitute for professional medical advice.' "
    "Keep your answer concise (maximum three sentences) and do not provide a definitive diagnosis. "
    "If you are unsure, say that you do not have enough information."
)

# Define the application state using a TypedDict
from langgraph.graph import START, StateGraph
from typing_extensions import TypedDict, List

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

# ---------------------------
# Define the Medical RAG Pipeline
# ---------------------------
def retrieve(state: State) -> State:
    """Retrieve the most relevant document chunks from the medical reference."""
    # Retrieve top 2 most relevant chunks based on the question.
    retrieved_docs = vector_store.similarity_search(state["question"], k=2)
    return {"question": state["question"], "context": retrieved_docs}

def generate(state: State) -> State:
    """Generate an answer based on the retrieved context and medical instructions."""
    # Combine the content from the retrieved documents.
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    
    # Create conversation messages including a system message with instructions and context,
    # then add the user's question as a user message.
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
def appointment_booking(state: State) -> State:
    """
    A simple appointment booking function.
    Here we ask the user for appointment details and simulate a booking confirmation.
    """
    details = input("Please enter your preferred appointment details (e.g., date, time, or any other notes): ")
    confirmation = (
        f"Your appointment has been booked for {details}. "
        "Please check your email for confirmation details. "
        "This information is for educational purposes and does not confirm an actual booking."
    )
    return {"question": state["question"], "context": [], "answer": confirmation}

# ---------------------------
# Main Conversation Loop
# ---------------------------
def main():
    print("Welcome to the Medical Chatbot!")
    print("Type your medical question or type 'appointment' to book an appointment.")
    print("Enter 'exit' to quit.")
    
    while True:
        # Accept user input continuously.
        user_input = input("\nYour message: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Decide which flow to follow based on the user's message.
        # Here we simply check if the user's message contains keywords for booking.
        if "appointment" in user_input.lower() or "book" in user_input.lower():
            # Run the appointment booking branch.
            result = appointment_booking({"question": user_input, "context": []})
        else:
            # Run the medical retrieval and generation pipeline.
            result = medical_graph.invoke({"question": user_input})
        
        # Print the chatbot's answer.
        print("\nChatbot:", result["answer"])

if __name__ == "__main__":
    main()
