# MCP Server

A FastMCP-powered server for advanced file operations, code review, API integration, and more. This server exposes a set of tools and resources via HTTP endpoints, making it easy to automate and interact with your workspace.

---

## Features

- **File Operations:** Create, read, list, and delete files.
- **Code Review:** Automated code review agent for Python and ML code, including PEP8 checks and custom instruction validation.
- **API Integration:** Tools for weather, JSON processing, and more.
- **Prompts & Resources:** Data analysis prompts, server info, and extensible endpoints.

---

## Setup

### 1. Clone the repository

```sh
git clone <your-repo-url>
cd mcp-server
```

### 2. Create and activate a virtual environment

```sh
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```sh
pip install -r requirements.txt
```

### 4. Set up environment variables

If your tools require API keys, create a `.env` file in the project root:

```
API_KEY=your_api_key_here
```

---

## Usage

### Start the server

```sh
python main_serve.py
```

The server will start and expose endpoints at `http://localhost:8000` (default).

---

## Example cURL Commands

**Create a file**
```sh
curl -X POST http://localhost:8000/tool/create_file \
     -H "Content-Type: application/json" \
     -d '{"filename": "example.txt", "content": "Hello, MCP!"}'
```

**Read a file**
```sh
curl -X POST http://localhost:8000/tool/read_file \
     -H "Content-Type: application/json" \
     -d '{"filename": "example.txt"}'
```

**List files**
```sh
curl -X POST http://localhost:8000/tool/list_files
```

**Delete a file**
```sh
curl -X POST http://localhost:8000/tool/delete_file \
     -H "Content-Type: application/json" \
     -d '{"filename": "example.txt"}'
```

**Get PEP8 coding styles**
```sh
curl -X POST http://localhost:8000/tool/get_pep8_coding_styles
```

**Get server info**
```sh
curl -X GET http://localhost:8000/resource/server://info
```

---

## Extending the Server

- Add new tools by defining functions and registering them with FastMCP.
- Add new resources or prompts for custom workflows.
- Integrate with external APIs by adding new endpoints.

---

## License

MIT License

---

## Support

For issues or feature requests, open an