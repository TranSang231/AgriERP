from datetime import timedelta
from django.utils import timezone


class BotFilterBackend():
    def filter_queryset(self, request, queryset, view):
        kwargs = view.kwargs
        bot_id = kwargs.get('bot_pk', None)
        if bot_id is not None:
            return queryset.filter(bot__id__in=bot_id)
        return queryset
