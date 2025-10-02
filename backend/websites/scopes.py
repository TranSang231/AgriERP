default_scopes = {
}

approvable_scopes = {
    "websites:sites:view": "View my business sites's sites",
    "websites:sites:edit": "Edit my business sites's sites",
    "websites:articles:view": "View my business's articles",
    "websites:articles:edit": "Edit my business's articles",
}

scopes = {}
scopes.update(default_scopes)
scopes.update(approvable_scopes)
