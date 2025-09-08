from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from graph.graph import app as graph_app
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import traceback
import uvicorn
import os
import importlib
import time
import threading

load_dotenv()

app = FastAPI()

# Track processing status of files
processing_files = {}

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str

# File watcher class
class DocumentHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            print(f"\nNew file detected: {filename}")

            # Mark file as processing
            processing_files[filename] = "processing"

            try:
                # Add a small delay to ensure file is completely written
                time.sleep(1)
                # Reimport and run ingestion
                import ingestion
                importlib.reload(ingestion)
                print("Ingestion process completed")
                # Mark file as completed
                processing_files[filename] = "completed"
            except Exception as e:
                print(f"Error processing file: {str(e)}")
                processing_files[filename] = f"error: {str(e)}"

# Start file watcher
def start_file_watcher():
    data_dir = "./data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    event_handler = DocumentHandler()
    observer = Observer()
    observer.schedule(event_handler, data_dir, recursive=False)
    observer.start()
    print(f"\nFile watcher started for directory: {data_dir}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Start file watcher in a separate thread
watcher_thread = threading.Thread(target=start_file_watcher, daemon=True)
watcher_thread.start()

@app.options("/chat")
async def chat_options():
    return {}

@app.post("/chat")
async def chat(request: QuestionRequest):
    try:
        # Use your existing graph
        inputs = {"question": request.question}
        response = ""

        # Execute the graph and get the final result
        result = graph_app.invoke(inputs)
        
        # Extract the final generation from the result
        if result and "generation" in result:
            response = result["generation"]

        return {"answer": response}
    except Exception as e:
        print(f"Error in /chat endpoint: {str(e)}")
        print("Traceback:")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/documents/upload")
async def upload_document(file: UploadFile):
    try:
        # Create data directory if it doesn't exist
        os.makedirs("./data", exist_ok=True)

        # Save the file
        file_path = f"./data/{file.filename}"
        print(f"Saving file to: {file_path}")

        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        return {"message": "File uploaded successfully"}

    except Exception as e:
        print(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
async def list_documents():
    try:
        docs_dir = "./data"
        if not os.path.exists(docs_dir):
            os.makedirs(docs_dir)

        # Get list of files with their processing status
        files = []
        for filename in os.listdir(docs_dir):
            status = processing_files.get(filename, "completed")  # Default to completed for existing files
            files.append({
                "name": filename,
                "status": status
            })

        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Test endpoint to verify server is running
@app.get("/")
async def root():
    return {"status": "ok", "message": "Server is running"}

@app.get("/test")
async def test():
    return {"status": "ok", "message": "Backend is reachable"}

# List all available routes for debugging
@app.get("/routes")
async def list_routes():
    routes = [
        {
            "path": route.path,
            "name": route.name,
            "methods": route.methods
        }
        for route in app.routes
    ]
    return {"routes": routes}

@app.delete("/documents/{filename}")
async def delete_document(filename: str):
    try:
        file_path = f"./data/{filename}"
        if os.path.exists(file_path):
            os.remove(file_path)
            # Remove from processing status if it exists
            if filename in processing_files:
                del processing_files[filename]
            return {"message": f"File {filename} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail=f"File {filename} not found")
    except Exception as e:
        print(f"Error deleting file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)