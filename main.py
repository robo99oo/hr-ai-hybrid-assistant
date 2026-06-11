from datetime import datetime

leaves = {}


def apply_leave(name: str = "Employee", days: int = 2, reason: str = "Auto request from Agentic HR OS") -> str:
    leaves.setdefault(name, []).append({
        "days": days,
        "reason": reason,
        "status": "Pending",
        "date": str(datetime.now())
    })

    return f"Leave applied for {name}"


def check_leave(name: str):
    return leaves.get(name, [])


def approve_leave(name: str):
    if name not in leaves:
        return "No records"

    for leave in leaves[name]:
        leave["status"] = "Approved"

    return f"Approved leaves for {name}"


def ping():
    return "MCP-style leave tool is working!"