default_scopes = {
    "employees:view-mine": "View my information",
    "employees:edit-mine": "Edit my information",
    "employees:view-public": "View employees's public information",
    "employees:view": "View my employees's information",
    "employees:edit": "Edit my employees's information"
}

approvable_scopes = {
    "employees:view": "View my employees's information",
    "employees:edit": "Edit my employees's information"
}

scopes = {}
scopes.update(default_scopes)
scopes.update(approvable_scopes)
