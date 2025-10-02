class UserTokenFilterBackend():
    def filter_queryset(self, request, queryset, view):
        user_id = request.auth.user.id
        return queryset.filter(user_id=user_id)
