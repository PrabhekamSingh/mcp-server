import asyncio
from fastmcp import Client

client = Client("http://127.0.0.1:8000/mcp")

async def call_tool():
    async with client:
        result = await client.call_tool("get_pep8_coding_styles")
        print(result)

asyncio.run(call_tool())