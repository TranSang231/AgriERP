from ..constants import AccessMode

class PublicAcessFilterBackend():
    def filter_queryset(self, request, queryset, view):
        if request.auth is None:
            ModelClass = queryset.model
            filter_field = (
                'namespace__access'
                if ModelClass is not None and getattr(ModelClass, 'namespace', None) is not None
                else 'access'
            )
            filter_kwargs = {filter_field: AccessMode.PUBLIC}
            return queryset.filter(**filter_kwargs)
        return queryset
