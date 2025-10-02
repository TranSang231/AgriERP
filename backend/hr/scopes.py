default_scopes = {
    "offices:view": "View my business's offices",
    "organization:view": "View my business's offices"
}

approvable_scopes = {
    "offices:edit": "Edit my business's offices",
    "organization:edit": "Edit my business's offices"
}

scopes = {}
scopes.update(default_scopes)
scopes.update(approvable_scopes)
