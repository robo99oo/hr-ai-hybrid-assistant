from mcp.server.fastmcp import FastMCP
from datetime import datetime

mcp = FastMCP("HR Assistant MCP", json_response=True)

leaves = {}

@mcp.tool()
def apply_leave(name: str, days: int, reason: str) -> str:
    leaves.setdefault(name, []).append({
        "days": days,
        "reason": reason,
        "status": "Pending",
        "date": str(datetime.now())
    })
    return f"Leave applied for {name}"


@mcp.resource("test://ping")
def ping():
    return "MCP server is working!"
@mcp.tool()
def check_leave(name: str):
    return leaves.get(name, [])

@mcp.tool()
def approve_leave(name: str):
    if name not in leaves:
        return "No records"
    for l in leaves[name]:
        l["status"] = "Approved"
    return f"Approved leaves for {name}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")