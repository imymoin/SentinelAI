ALLOWED_TOOLS = {
    "file_get_project_info",
    "file_get_project_status",
    "db_get_employee",
    "db_get_project_status",
    "db_get_team_members",
}


def validate_tool(tool_name: str) -> tuple[bool, str]:
    """Validate whether the MCP tool is authorized."""

    if tool_name not in ALLOWED_TOOLS:
        return False, f"Tool '{tool_name}' is not authorized."

    return True, "Tool authorized."


def validate_tool_arguments(
    tool_name: str,
    arguments: dict
) -> tuple[bool, str]:
    """Validate arguments before executing an MCP tool."""

    # Ensure arguments are a dictionary
    if not isinstance(arguments, dict):
        return False, "Tool arguments must be a dictionary."

    # Employee lookup validation
    if tool_name == "db_get_employee":

        employee_id = arguments.get("employee_id")

        if not employee_id:
            return False, "employee_id is required."

        if not str(employee_id).isdigit():
            return False, "employee_id must contain only numbers."

        return True, "Employee ID validated."

    # Project tools validation
    if tool_name in [
        "db_get_project_status",
        "db_get_team_members",
    ]:

        project_name = arguments.get("project_name")

        if not project_name:
            return False, "project_name is required."

        if not isinstance(project_name, str):
            return False, "project_name must be a string."

        # Prevent suspiciously long input
        if len(project_name) > 100:
            return False, "project_name is too long."

        return True, "Project name validated."

    # File tools currently don't require arguments
    if tool_name in [
        "file_get_project_info",
        "file_get_project_status",
    ]:

        if arguments:
            return False, f"{tool_name} does not accept arguments."

        return True, "No arguments required."

    return False, "Unknown tool configuration."