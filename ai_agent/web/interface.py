"""Web interface for the AI Agent."""

import os
import logging
from typing import Optional
from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from ..core.agent import AIAgent
from ..core.config import Config


class WebInterface:
    """Web interface for the AI Agent."""
    
    def __init__(self, agent: AIAgent, config: Config):
        """Initialize the web interface."""
        self.agent = agent
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Create FastAPI app
        self.app = FastAPI(
            title="AI Agent for Blind Users",
            description="Accessible AI assistant web interface",
            version="1.0.0"
        )
        
        # Setup templates and static files
        self.templates = Jinja2Templates(directory="templates")
        
        # Mount static files if directory exists
        if os.path.exists("static"):
            self.app.mount("/static", StaticFiles(directory="static"), name="static")
        
        self._setup_routes()
    
    def _setup_routes(self):
        """Set up web routes."""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def home(request: Request):
            """Home page."""
            return self.templates.TemplateResponse(
                "index.html", 
                {"request": request, "title": "AI Agent for Blind Users"}
            )
        
        @self.app.post("/process_text")
        async def process_text(text: str = Form(...)):
            """Process text input and return response."""
            try:
                response = await self.agent.process_text_command(text)
                return JSONResponse({"response": response, "success": True})
            except Exception as e:
                self.logger.error(f"Error processing text: {e}")
                return JSONResponse({
                    "response": "I encountered an error processing your request.",
                    "success": False
                }, status_code=500)
        
        @self.app.post("/voice_command")
        async def voice_command():
            """Process voice command."""
            try:
                response = await self.agent.process_voice_command()
                return JSONResponse({
                    "response": response or "No speech detected",
                    "success": True
                })
            except Exception as e:
                self.logger.error(f"Error processing voice command: {e}")
                return JSONResponse({
                    "response": "I encountered an error processing your voice command.",
                    "success": False
                }, status_code=500)
        
        @self.app.post("/analyze_image")
        async def analyze_image(file: UploadFile = File(...)):
            """Analyze uploaded image."""
            try:
                # Save uploaded file temporarily
                temp_path = f"temp/{file.filename}"
                os.makedirs("temp", exist_ok=True)
                
                with open(temp_path, "wb") as buffer:
                    content = await file.read()
                    buffer.write(content)
                
                # Analyze image
                description = await self.agent.analyze_image(temp_path)
                
                # Clean up temp file
                try:
                    os.remove(temp_path)
                except:
                    pass
                
                return JSONResponse({
                    "description": description,
                    "success": True
                })
                
            except Exception as e:
                self.logger.error(f"Error analyzing image: {e}")
                return JSONResponse({
                    "description": "I encountered an error analyzing the image.",
                    "success": False
                }, status_code=500)
        
        @self.app.get("/history")
        async def get_history():
            """Get session history."""
            try:
                history = self.agent.get_session_history()
                return JSONResponse({"history": history, "success": True})
            except Exception as e:
                self.logger.error(f"Error getting history: {e}")
                return JSONResponse({
                    "history": [],
                    "success": False
                }, status_code=500)
        
        @self.app.post("/clear_history")
        async def clear_history():
            """Clear session history."""
            try:
                self.agent.clear_session_history()
                return JSONResponse({"message": "History cleared", "success": True})
            except Exception as e:
                self.logger.error(f"Error clearing history: {e}")
                return JSONResponse({
                    "message": "Error clearing history",
                    "success": False
                }, status_code=500)
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint."""
            return JSONResponse({"status": "healthy", "success": True})
    
    def run(self):
        """Run the web interface."""
        self.logger.info(f"Starting web interface on {self.config.web_host}:{self.config.web_port}")
        uvicorn.run(
            self.app,
            host=self.config.web_host,
            port=self.config.web_port,
            log_level="info" if self.config.debug_mode else "warning"
        )