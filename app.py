import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from graph.graph import app 
from ingestion import parser, vectorstore, text_splitter
from langchain.schema import Document
load_dotenv()

# Initialize Streamlit app
st.title("Course Material Q&A")

# Sidebar for file management
with st.sidebar:
    st.header("Document Management")
    
    # Show current files
    st.subheader("Current Documents")
    docs_dir = "./data"
    if os.path.exists(docs_dir):
        files = [f for f in os.listdir(docs_dir) if f.endswith(('.pdf', '.docx', '.txt'))]
        for file in files:
            st.text(f"📄 {file}")
    
    # File uploader
    st.subheader("Add New Document")
    uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx', 'txt'])
    
    if uploaded_file is not None:
        # Save uploaded file
        save_path = os.path.join(docs_dir, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Process new file
        with st.spinner(f"Processing {uploaded_file.name}..."):
            try:
                parsed_doc = parser.load_data(str(save_path))
                converted_docs = [
                    Document(
                        page_content=doc.text if hasattr(doc, 'text') else str(doc),
                        metadata=doc.metadata if hasattr(doc, 'metadata') else {}
                    )
                    for doc in parsed_doc
                ]
                doc_splits = text_splitter.split_documents(converted_docs)
                
                # Update vectorstore
                vectorstore.add_documents(doc_splits)
                st.success(f"Successfully processed {uploaded_file.name}")
            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                # Clean up failed upload
                os.remove(save_path)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.thread_id = "1"

# Chat interface
user_input = st.chat_input("Ask a question about your course materials:")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Create a placeholder for the "thinking" message
    with st.chat_message("assistant"):
        thinking_placeholder = st.empty()
        thinking_placeholder.text("Thinking...")
        
        try:
            # Prepare input for graph
            inputs = {"question": user_input}
            
            # Get response from graph
            for output in app.stream(inputs, config={"configurable": {"thread_id": st.session_state.thread_id}}):
                for key, value in output.items():
                    if "generation" in value:
                        # Clear the "thinking" message
                        thinking_placeholder.empty()
                        # Add assistant response to chat history
                        st.session_state.messages.append(
                            {"role": "assistant", "content": value["generation"]}
                        )
        except Exception as e:
            thinking_placeholder.error(f"An error occurred: {str(e)}")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Add requirements to requirements.txt 