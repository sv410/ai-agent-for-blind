"""FastAPI application entry point for deployment."""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from deploy_agent import AIAgent, Config

# Create configuration
config = Config.from_env()
config.debug_mode = False
config.web_port = int(os.environ.get("PORT", 8000))
config.web_host = "0.0.0.0"

# Create AI agent
agent = AIAgent(config)

# Create FastAPI app
app = FastAPI(
    title="AI Agent for Blind Users",
    description="Accessible AI assistant web interface",
    version="1.0.0"
)

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Agent for Blind Users</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px; 
            background-color: #f0f0f0;
        }
        .container { 
            background: white; 
            padding: 20px; 
            border-radius: 10px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        input, button { 
            font-size: 16px; 
            padding: 10px; 
            margin: 10px 5px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        input[type="text"] { 
            width: 60%; 
            min-width: 300px;
        }
        button { 
            background: #007cba; 
            color: white; 
            border: none; 
            cursor: pointer; 
            min-width: 100px;
        }
        button:hover { 
            background: #005a87; 
        }
        .response { 
            background: #f8f9fa; 
            padding: 15px; 
            margin: 10px 0; 
            border-radius: 5px; 
            border-left: 4px solid #007cba;
        }
        h1 { color: #007cba; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AI Agent for Blind Users</h1>
        <p>Accessible AI assistant designed for blind and visually impaired users.</p>
        
        <div>
            <h3>💬 Text Commands</h3>
            <form id="textForm">
                <input type="text" id="textInput" placeholder="Type your message here..." required>
                <button type="submit">Send</button>
            </form>
            <div id="response" class="response" style="display: none;"></div>
        </div>
        
        <div>
            <h3>ℹ️ Try These Commands</h3>
            <ul>
                <li>"Hello" - Get a friendly greeting</li>
                <li>"What time is it?" - Get the current time</li>
                <li>"Help" - See all available commands</li>
            </ul>
        </div>
    </div>

    <script>
        document.getElementById('textForm').onsubmit = async function(e) {
            e.preventDefault();
            const input = document.getElementById('textInput');
            const response = document.getElementById('response');
            
            if (!input.value.trim()) return;
            
            response.style.display = 'block';
            response.innerHTML = '<p>Processing...</p>';
            
            try {
                const formData = new FormData();
                formData.append('text', input.value);
                
                const res = await fetch('/process_text', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await res.json();
                response.innerHTML = '<strong>Response:</strong><br><br>' + data.response.replace(/\\n/g, '<br>');
                input.value = '';
                input.focus();
            } catch (error) {
                response.innerHTML = '<strong>Error:</strong> Failed to process request.';
            }
        };
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(HTML_TEMPLATE)

@app.post("/process_text")
async def process_text(text: str = Form(...)):
    try:
        response = await agent.process_text_command(text)
        return JSONResponse({"response": response, "success": True})
    except Exception as e:
        return JSONResponse({
            "response": "Error processing request.",
            "success": False
        }, status_code=500)

@app.get("/health")
async def health_check():
    return JSONResponse({"status": "healthy", "success": True})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))