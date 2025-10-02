default_scopes = {
    "knowledge:namespaces:view-mine": "View my namespaces",
    "knowledge:namespaces:edit-mine": "Edit my namespaces",
    "knowledge:pages:view-mine": "View my pages",
    "knowledge:pages:edit-mine": "Edit my pages",
}

approvable_scopes = {
    "knowledge:namespaces:view": "View all namespaces",
    "knowledge:namespaces:edit": "Edit all namespaces",
    "knowledge:pages:view": "View all pages",
    "knowledge:pages:edit": "Edit all pages",
}

scopes = {}
scopes.update(default_scopes)
scopes.update(approvable_scopes)
