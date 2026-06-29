ROLES = {
    "admin": {"read", "write", "delete", "manage_users", "view_dashboard", "run_query"},
    "analyst": {"read", "view_dashboard", "run_query"},
    "operator": {"read", "write", "view_dashboard"},
    "viewer": {"read", "view_dashboard"},
}


class AccessDenied(Exception):
    pass


def get_permissions(role):
    return ROLES.get(role, set())


def has_permission(role, permission):
    return permission in get_permissions(role)


def require_permission(role, permission):
    if not has_permission(role, permission):
        raise AccessDenied(f"Role '{role}' tidak punya izin '{permission}'")
    return True


if __name__ == "__main__":
    print(has_permission("analyst", "run_query"))  # True
    print(has_permission("viewer", "delete"))       # False
