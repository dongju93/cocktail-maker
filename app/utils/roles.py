def check_roles(user_roles: list[str], required_roles: list[str]) -> bool:
    return any(role in required_roles for role in user_roles)
