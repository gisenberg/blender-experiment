"""Exercise the real MCP stdio connection to the interactive Blender session."""
import asyncio
import base64
import json
import os
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]


async def main():
    output = ROOT / "outputs"
    output.mkdir(exist_ok=True)
    params = StdioServerParameters(
        command=str(ROOT / ".tools/blender-mcp-venv/Scripts/python.exe"),
        args=["-m", "blmcp"],
        env={**os.environ, "BLENDER_MCP_HOST": "127.0.0.1"},
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            catalog = await session.list_tools()
            print(f"MCP initialized: {len(catalog.tools)} tools")

            async def call(name, args):
                response = await session.call_tool(name, args)
                assert not response.isError, response
                return response

            summary = await call("get_objects_summary", {})
            (output / "scene-summary.json").write_text(
                summary.model_dump_json(indent=2), encoding="utf-8"
            )
            print("Scene inspection passed")
            response = await call("execute_blender_code", {"code": """
import bpy
mesh = bpy.data.meshes.new('MCPConnectionTest')
obj = bpy.data.objects.new('MCPConnectionTest', mesh)
bpy.context.scene.collection.objects.link(obj)
obj.location = (1.0, 2.0, 3.0)
verified = tuple(obj.location) == (1.0, 2.0, 3.0)
bpy.data.objects.remove(obj, do_unlink=True)
bpy.data.meshes.remove(mesh)
result = {'created_moved_and_removed': verified, 'blender_version': bpy.app.version_string}
"""})
            payload = json.loads(next(b.text for b in response.content if b.type == "text"))
            assert payload["status"] == "ok", payload
            assert payload["result"]["created_moved_and_removed"] is True, payload
            print(json.dumps(payload))
            screenshot = await call("get_screenshot_of_window_as_image", {})
            block = next(b for b in screenshot.content if b.type == "image")
            (output / "blender-mcp.png").write_bytes(base64.b64decode(block.data))
            print("Screenshot saved; MCP verification passed")


asyncio.run(main())
