default_scopes = {
    "contents:view-mine": "View my created contents",
    "contents:edit-mine": "Edit my created contents",
}

approvable_scopes = {
    "contents:view": "View my business contents",
    "contents:edit-mine": "Edit my business contents",
}

scopes = {}
scopes.update(default_scopes)
scopes.update(approvable_scopes)