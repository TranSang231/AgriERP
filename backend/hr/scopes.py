default_scopes = {
    "offices:view": "View my business's offices",
    "organization:view": "View my business's offices",
    "timekeeping:view": "View timekeeping records",
    "timekeeping:check": "Check in/out for timekeeping"
}

approvable_scopes = {
    "offices:edit": "Edit my business's offices",
    "organization:edit": "Edit my business's offices",
    "timekeeping:edit": "Edit timekeeping records",
    "timekeeping:manage": "Manage all timekeeping records"
}

scopes = {}
scopes.update(default_scopes)
scopes.update(approvable_scopes)
