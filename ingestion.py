import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from llama_parse import LlamaParse
from langchain.schema import Document
import torch
import shutil

load_dotenv()

parsing_instruction = """Parse university-level engineering coursebooks with the following requirements:

Document Structure:
- Maintain original document hierarchy and chapter organization
- Preserve table of contents and its structure
- Split content according to the sections defined in the contents page
- Keep title pages intact

Content Elements to Extract:
- Main text content
- Mathematical formulae (preserve formatting)
- Figures, graphs, and diagrams
- Tables and data
- Important definitions and theorems
- References and citations

Typography and Formatting:
- Maintain heading levels based on font sizes
- Keep subscripts and superscripts in mathematical notation
- Preserve special characters and symbols
- Maintain font-based emphasis (e.g., bold terms in definitions)
- Retain font-based hierarchical structure (e.g., larger fonts for headers)
- Keep Greek letters and mathematical symbols intact
- Preserve indentation and list formatting

Special Handling:
- Preserve all academic terminology without simplification
- Maintain relationships between formulas and their explanations
- Keep figure captions with their corresponding images
- Preserve formatting of mathematical symbols and equations
- Handle multi-column layouts appropriately

Output Format:
- Return a structured output maintaining document hierarchy
- Include metadata for each section (chapter number, title, etc.)
- Preserve cross-references between sections
- Tag special elements (theorems, definitions, examples)
- Include page numbers for all extracted content
- Track source locations (page numbers, sections) for all information
"""

parser = LlamaParse(
    api_key=os.getenv("LLAMA_CLOUD_API_KEY"),
    parsing_instruction=parsing_instruction,
    result_type="markdown"
)

docs_dir = "./data"

files = [
    os.path.join(docs_dir, f)
    for f in os.listdir(docs_dir)
    if f.endswith(('.pdf', '.docx', '.txt'))  
]
docs = []
for file in files:
    try:
        parsed_doc = parser.load_data(str(file))
        converted_docs = [
            Document(
                page_content=doc.text if hasattr(doc, 'text') else str(doc),
                metadata=doc.metadata if hasattr(doc, 'metadata') else {}
            )
            for doc in parsed_doc
        ]
        docs.extend(converted_docs)
        print(f"Successfully processed {file}")
    except Exception as e:
        print(f"Error processing {file}: {str(e)}")

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=1000,
    chunk_overlap=100,
    model_name="gpt-4o-mini"
)
doc_splits = text_splitter.split_documents(docs)

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-en-v1.5",
    model_kwargs={'device': 'cuda' if torch.cuda.is_available() else 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)


if os.path.exists("./.chroma"):
    shutil.rmtree("./.chroma")


vectorstore = Chroma.from_documents(
    documents=doc_splits,
    collection_name="rag-chroma",
    embedding=embeddings,
    persist_directory="./.chroma",
)

retriever = Chroma(
    collection_name="rag-chroma",
    persist_directory="./.chroma",
    embedding_function=embeddings,
).as_retriever()