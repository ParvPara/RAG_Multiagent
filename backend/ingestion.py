import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from llama_parse import LlamaParse
from langchain.schema import Document
import tiktoken
from qdrant_client import QdrantClient
from qdrant_client.http import models

load_dotenv()

# Get Qdrant cloud credentials from environment variables
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "COMPENDAI_COLLECTION"

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

# Ensure the data directory exists
os.makedirs(docs_dir, exist_ok=True)

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

embeddings = OpenAIEmbeddings()

def process_documents(file_paths):
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000,
        chunk_overlap=100,
        encoding_name="cl100k_base"
    )
    doc_splits = text_splitter.split_documents(docs)
    
    # Create Qdrant client
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    
    # Get embeddings for documents
    texts = [doc.page_content for doc in doc_splits]
    metadatas = [doc.metadata for doc in doc_splits]
    embeddings_vectors = embeddings.embed_documents(texts)
    
    # Create or recreate collection
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=len(embeddings_vectors[0]),
            distance=models.Distance.COSINE
        )
    )
    
    # Upload documents with their embeddings
    client.upload_points(
        collection_name=COLLECTION_NAME,
        points=[
            models.PointStruct(
                id=i,
                vector=embedding,
                payload={"text": text, "metadata": metadata}
            )
            for i, (text, embedding, metadata) in enumerate(zip(texts, embeddings_vectors, metadatas))
        ]
    )
    
    return client

if docs:  # Only process if we have documents
    client = process_documents(docs)
else:
    print("No documents found in data directory. Vector store will be created when documents are added.")
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

# Create retriever function
def retrieve_similar(query: str, k: int = 4):
    # Get query embedding
    query_vector = embeddings.embed_query(query)
    
    # Search in Qdrant
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=k
    )
    
    # Return documents
    return [
        Document(
            page_content=hit.payload["text"],
            metadata=hit.payload["metadata"]
        )
        for hit in results
    ]

retriever = retrieve_similar