#!/usr/bin/env python3
"""
Advanced MCP Server Example
Demonstrates file operations, external API calls, and complex data handling.
"""

import asyncio
import json
import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import httpx
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent, ImageContent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("advanced-mcp-server")

# Create the MCP server instance
mcp = FastMCP("Advanced File & API Server")

# Configuration
WORK_DIR = Path("./mcp_workspace")
WORK_DIR.mkdir(exist_ok=True)

# File operations tools
@mcp.tool()
def create_file(filename: str, content: str) -> Dict[str, Any]:
    """Create a new file with the given content.
    
    Args:
        filename: Name of the file to create
        content: Content to write to the file
        
    Returns:
        Dictionary with operation result
    """
    try:
        file_path = WORK_DIR / filename
        
        # Ensure we don't overwrite existing files accidentally
        if file_path.exists():
            return {
                "success": False,
                "error": f"File {filename} already exists",
                "path": str(file_path)
            }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "success": True,
            "message": f"File {filename} created successfully",
            "path": str(file_path),
            "size": len(content)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to create file: {str(e)}"
        }

@mcp.tool()
def read_file(filename: str) -> Dict[str, Any]:
    """Read the content of a file.
    
    Args:
        filename: Name of the file to read
        
    Returns:
        Dictionary with file content or error
    """
    try:
        file_path = WORK_DIR / filename
        
        if not file_path.exists():
            return {
                "success": False,
                "error": f"File {filename} does not exist"
            }
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            "success": True,
            "filename": filename,
            "content": content,
            "size": len(content),
            "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to read file: {str(e)}"
        }

@mcp.tool()
def list_files() -> Dict[str, Any]:
    """List all files in the workspace directory.
    
    Returns:
        Dictionary with list of files and their info
    """
    try:
        files = []
        for file_path in WORK_DIR.iterdir():
            if file_path.is_file():
                stat = file_path.stat()
                files.append({
                    "name": file_path.name,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "path": str(file_path)
                })
        
        return {
            "success": True,
            "files": files,
            "count": len(files),
            "workspace": str(WORK_DIR)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to list files: {str(e)}"
        }

@mcp.tool()
def delete_file(filename: str) -> Dict[str, Any]:
    """Delete a file from the workspace.
    
    Args:
        filename: Name of the file to delete
        
    Returns:
        Dictionary with operation result
    """
    try:
        file_path = WORK_DIR / filename
        
        if not file_path.exists():
            return {
                "success": False,
                "error": f"File {filename} does not exist"
            }
        
        file_path.unlink()
        
        return {
            "success": True,
            "message": f"File {filename} deleted successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to delete file: {str(e)}"
        }

# External API tools
@mcp.tool()
async def get_weather(city: str) -> Dict[str, Any]:
    """Get current weather information for a city.
    
    Args:
        city: Name of the city
        
    Returns:
        Dictionary with weather information
    """
    try:
        # Using a free weather API (OpenWeatherMap alternative)
        # Note: In production, you'd want to use a proper API key
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": "demo_key",  # Replace with actual API key
            "units": "metric"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "city": data.get("name"),
                    "country": data.get("sys", {}).get("country"),
                    "temperature": data.get("main", {}).get("temp"),
                    "description": data.get("weather", [{}])[0].get("description"),
                    "humidity": data.get("main", {}).get("humidity"),
                    "pressure": data.get("main", {}).get("pressure")
                }
            else:
                return {
                    "success": False,
                    "error": f"Weather API error: {response.status_code}"
                }
    except Exception as e:
        # Fallback to mock data for demo purposes
        return {
            "success": True,
            "city": city,
            "temperature": 22,
            "description": "partly cloudy",
            "humidity": 65,
            "pressure": 1013,
            "note": "Demo data - API key needed for real data"
        }

@mcp.tool()
async def get_random_quote() -> Dict[str, Any]:
    """Get a random inspirational quote.
    
    Returns:
        Dictionary with quote and author
    """
    try:
        url = "https://api.quotable.io/random"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "quote": data.get("content"),
                    "author": data.get("author"),
                    "tags": data.get("tags", [])
                }
            else:
                return {
                    "success": False,
                    "error": f"Quote API error: {response.status_code}"
                }
    except Exception as e:
        # Fallback quotes
        quotes = [
            {"quote": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
            {"quote": "Innovation distinguishes between a leader and a follower.", "author": "Steve Jobs"},
            {"quote": "Life is what happens to you while you're busy making other plans.", "author": "John Lennon"}
        ]
        import random
        selected = random.choice(quotes)
        return {
            "success": True,
            "quote": selected["quote"],
            "author": selected["author"],
            "note": "Fallback quote - API unavailable"
        }

# Data processing tools
@mcp.tool()
def process_json_data(json_string: str) -> Dict[str, Any]:
    """Process and validate JSON data.
    
    Args:
        json_string: JSON string to process
        
    Returns:
        Dictionary with processed data or error
    """
    try:
        data = json.loads(json_string)
        
        # Analyze the JSON structure
        analysis = {
            "type": type(data).__name__,
            "size": len(json_string),
            "keys": list(data.keys()) if isinstance(data, dict) else None,
            "length": len(data) if isinstance(data, (list, dict)) else None,
            "nested_levels": _count_nested_levels(data)
        }
        
        return {
            "success": True,
            "data": data,
            "analysis": analysis,
            "valid": True
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"Invalid JSON: {str(e)}",
            "valid": False
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Processing error: {str(e)}"
        }

def _count_nested_levels(obj, level=0):
    """Helper function to count nesting levels in JSON."""
    if isinstance(obj, dict):
        if not obj:
            return level
        return max(_count_nested_levels(v, level + 1) for v in obj.values())
    elif isinstance(obj, list):
        if not obj:
            return level
        return max(_count_nested_levels(item, level + 1) for item in obj)
    else:
        return level

# Resource for providing server information
@mcp.resource("server://info")
def get_server_info() -> str:
    """Get information about this MCP server."""
    return f"""
    Advanced MCP Server Information
    ==============================
    
    Server Name: Advanced File & API Server
    Workspace: {WORK_DIR}
    Started: {datetime.now().isoformat()}
    
    Available Tools:
    - File Operations: create_file, read_file, list_files, delete_file
    - External APIs: get_weather, get_random_quote
    - Data Processing: process_json_data
    
    Available Resources:
    - server://info - This information page
    
    Available Prompts:
    - data_analysis_prompt - For analyzing data files
    - api_integration_prompt - For API integration guidance
    """

# Prompts for different use cases
@mcp.prompt()
def data_analysis_prompt(data_type: str, objective: str) -> str:
    """Generate a data analysis prompt.
    
    Args:
        data_type: Type of data to analyze (csv, json, text, etc.)
        objective: What you want to achieve with the analysis
    """
    return f"""
    You are a data analysis expert. Please help analyze {data_type} data with the following objective: {objective}
    
    Please provide:
    1. Initial data exploration steps
    2. Relevant statistical measures or metrics
    3. Visualization recommendations
    4. Key insights to look for
    5. Potential pitfalls or limitations to consider
    
    Make your analysis thorough but accessible to non-experts.
    """

@mcp.prompt()
def api_integration_prompt(api_name: str, use_case: str) -> str:
    """Generate an API integration prompt.
    
    Args:
        api_name: Name of the API to integrate
        use_case: Specific use case or goal
    """
    return f"""
    You are an API integration specialist. Please provide guidance for integrating {api_name} API for the following use case: {use_case}
    
    Please include:
    1. Authentication requirements
    2. Rate limiting considerations
    3. Error handling strategies
    4. Data transformation needs
    5. Testing approaches
    6. Security best practices
    
    Provide practical, production-ready advice.
    """

async def main():
    """Main function to run the advanced MCP server."""
    try:
        logger.info("Starting Advanced MCP server...")
        logger.info(f"Workspace directory: {WORK_DIR}")
        await mcp.run()
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())