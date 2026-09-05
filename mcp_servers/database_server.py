from mcp.server.fastmcp import FastMCP


mcp = FastMCP("SentinelAI Database Server")


employees = {
    "101": {
        "employee_id": "101",
        "name": "John Smith",
        "role": "Software Engineer",
        "department": "Engineering",
    },
    "102": {
        "employee_id": "102",
        "name": "Sarah Johnson",
        "role": "Data Analyst",
        "department": "Analytics",
    },
}


projects = {
    "sentinelai": {
        "project": "SentinelAI",
        "status": "In development",
        "team": ["101", "102"],
    }
}


@mcp.tool()
def db_get_employee(employee_id: str) -> dict:
    """Get employee information using employee ID."""

    if employee_id in employees:
        return employees[employee_id]

    return {
        "error": "Employee not found"
    }


@mcp.tool()
def db_get_project_status(project_name: str) -> dict:
    """Get project status using project name."""

    project_name = project_name.lower()

    if project_name in projects:
        return projects[project_name]

    return {
        "error": "Project not found"
    }


@mcp.tool()
def db_get_team_members(project_name: str) -> list:
    """Get team members working on a project."""

    project_name = project_name.lower()

    if project_name not in projects:
        return []

    team_ids = projects[project_name]["team"]

    return [
        employees[employee_id]
        for employee_id in team_ids
        if employee_id in employees
    ]


if __name__ == "__main__":
    mcp.run()