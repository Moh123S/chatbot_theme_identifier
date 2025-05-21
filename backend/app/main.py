import sys
import os
from pathlib import Path

# Debug: Print Python path and current directory
print("Python path:", sys.path)
print("Current directory:", os.getcwd())
print("GROQ_API_KEY before load_dotenv:", os.getenv("GROQ_API_KEY"))

# Add backend directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.api.routes import router as api_router
from dotenv import load_dotenv

# Load environment variables
env_path = os.path.join(os.getcwd(), ".env")
print("Looking for .env at:", env_path)
if os.path.exists(env_path):
    print(".env file exists")
    with open(env_path, 'r') as f:
        print(".env content:", f.read().strip())
else:
    print(".env file not found")
load_dotenv(env_path)
print("GROQ_API_KEY after load_dotenv:", os.getenv("GROQ_API_KEY"))

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="backend/static"), name="static")
templates = Jinja2Templates(directory="backend/templates")

# Include API router
app.include_router(api_router, prefix="/api")

# Serve the main web interface
@app.get("/", response_class=HTMLResponse)
async def index(request: fastapi.Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)