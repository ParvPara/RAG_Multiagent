# RAG Multiagent

A sophisticated Retrieval-Augmented Generation (RAG) system built with LangGraph that combines document retrieval, web search, and AI-powered question answering. This multiagent system intelligently routes queries through different processing paths to provide accurate and comprehensive answers.

## Features

- **Document Upload & Processing**: Upload PDF, DOCX, and TXT files for knowledge base creation
- **Intelligent Retrieval**: Advanced document retrieval using Qdrant vector database
- **Web Search Integration**: Automatic web search when documents don't contain sufficient information
- **Multiagent Architecture**: LangGraph-powered workflow with specialized agents for different tasks
- **Modern Web Interface**: Next.js frontend with real-time chat interface
- **Document Management**: Upload, view, and delete documents through the web interface

## Architecture

The system uses a multiagent approach with the following components:

1. **Retrieval Agent**: Searches through uploaded documents using semantic similarity
2. **Document Grader**: Evaluates relevance of retrieved documents to the user's question
3. **Generation Agent**: Creates answers based on retrieved documents
4. **Web Search Agent**: Performs web searches when documents are insufficient
5. **Hallucination Grader**: Ensures generated answers are grounded in the provided documents

## Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn
- Qdrant Cloud account
- OpenAI API key
- LlamaCloud API key (for document parsing)
- Tavily API key (for web search)

## Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the backend directory with the following variables:

```env
# OpenAI API Key (required for LLM operations)
OPENAI_API_KEY=your_openai_api_key_here

# Qdrant Cloud Configuration (required for vector database)
QDRANT_URL=your_qdrant_cloud_url_here
QDRANT_API_KEY=your_qdrant_api_key_here

# LlamaCloud API Key (required for document parsing)
LLAMA_CLOUD_API_KEY=your_llama_cloud_api_key_here

# Tavily API Key (required for web search)
TAVILY_API_KEY=your_tavily_api_key_here
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env.local` file in the frontend directory:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Access Key for Login (CHANGE THIS TO YOUR OWN SECURE KEY)
NEXT_PUBLIC_ACCESS_KEY=your-secure-access-key-here
```

**Important:** Replace `your-secure-access-key-here` with your own secure access key. This key will be used to authenticate users when they log into the application.

## Environment Variables Explained

### Backend (.env)

- **OPENAI_API_KEY**: Your OpenAI API key for GPT-4o-mini model access. Get it from [OpenAI Platform](https://platform.openai.com/api-keys)
- **QDRANT_URL**: Your Qdrant Cloud cluster URL. Get it from [Qdrant Cloud](https://cloud.qdrant.io/)
- **QDRANT_API_KEY**: Your Qdrant Cloud API key for authentication
- **LLAMA_CLOUD_API_KEY**: API key for LlamaParse service for document parsing. Get it from [LlamaIndex](https://cloud.llamaindex.ai/)
- **TAVILY_API_KEY**: API key for Tavily search service. Get it from [Tavily](https://tavily.com/)

### Frontend (.env.local)

- **NEXT_PUBLIC_API_URL**: The URL where your backend API is running (default: http://localhost:8000)
- **NEXT_PUBLIC_ACCESS_KEY**: Your secure access key for login authentication (CHANGE FROM DEFAULT)

**⚠️ Important Security Note:** The access key is used for simple authentication. Make sure to:
- Change the default key to something secure
- Use a strong, unique key for production
- Never commit your actual access key to version control
- Consider implementing proper authentication (JWT, OAuth) for production use

## Usage

### Starting the Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Activate your virtual environment:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Start the FastAPI server:
```bash
python main.py
```

The backend will be available at `http://localhost:8000`

### Starting the Frontend

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Start the Next.js development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Using the Application

1. Open your browser and navigate to `http://localhost:3000`
2. Upload documents (PDF, DOCX, TXT) using the file upload interface
3. Ask questions about your uploaded documents
4. The system will automatically:
   - Search through your documents
   - Perform web searches if needed
   - Generate comprehensive answers
   - Ensure answers are grounded in your documents

## API Endpoints

### Backend API

- `GET /documents` - List all uploaded documents
- `POST /documents/upload` - Upload a new document
- `DELETE /documents/{filename}` - Delete a document
- `POST /chat` - Send a question and get an answer

### Example API Usage

```bash
# Upload a document
curl -X POST "http://localhost:8000/documents/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_document.pdf"

# Ask a question
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic of the uploaded documents?"}'
```

## Project Structure

```
RAG_Multiagent-main/
├── backend/
│   ├── graph/                 # LangGraph workflow definitions
│   │   ├── chains/           # LLM chains for different tasks
│   │   ├── nodes/            # Graph nodes implementation
│   │   └── state.py          # Graph state management
│   ├── chroma_db/            # Local vector database (if using Chroma)
│   ├── main.py               # FastAPI application entry point
│   ├── ingestion.py          # Document processing and ingestion
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js app router pages
│   │   ├── components/       # React components
│   │   └── services/         # API service functions
│   └── package.json          # Node.js dependencies
└── README.md
```

## Development

### Running Tests

```bash
cd backend
python -m pytest graph/chains/tests/
```

### Code Formatting

```bash
cd backend
black .
isort .
```

## Deployment

The project includes configuration files for deployment:

- `Dockerfile` - For containerized deployment
- `render.yaml` - For Render.com deployment
- `Procfile` - For Heroku deployment

## Troubleshooting

### Common Issues

1. **Missing API Keys**: Ensure all required environment variables are set in your `.env` file
2. **Qdrant Connection Issues**: Verify your Qdrant Cloud URL and API key are correct
3. **Document Upload Fails**: Check that the file format is supported (PDF, DOCX, TXT)
4. **Frontend Can't Connect**: Verify `NEXT_PUBLIC_API_URL` points to your running backend
5. **Login Issues**: 
   - Make sure `NEXT_PUBLIC_ACCESS_KEY` is set in your `.env.local` file
   - Restart your frontend server after changing environment variables
   - Verify the access key matches what you're entering in the login form

### Getting API Keys

- **OpenAI**: Sign up at [OpenAI Platform](https://platform.openai.com/) and create an API key
- **Qdrant Cloud**: Create a free account at [Qdrant Cloud](https://cloud.qdrant.io/)
- **LlamaCloud**: Sign up at [LlamaIndex Cloud](https://cloud.llamaindex.ai/)
- **Tavily**: Get a free API key at [Tavily](https://tavily.com/)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.