# urls.py
from django.urls import path, include
from rest_framework_nested import routers
from .views import (
    BotViewSet,
    EntityViewSet,
    IntentViewSet,
    ExpressionViewSet,
    SynonymViewSet,
    RegexViewSet,
    ActionViewSet,
    ResponseViewSet,
    ConversationViewSet,
    NLUModelViewSet,
    StoryViewSet,
    RuleViewSet,
    UtteranceViewSet,
    NLUViewSet,
    NLUPublicViewSet
)

app_name = "va"
router = routers.SimpleRouter(trailing_slash=False)
router.register(r"bots", BotViewSet, basename="virtual-assistants-bots")
router.register(r"entities", EntityViewSet, basename="virtual-assistants-entities")
router.register(r"intents", IntentViewSet, basename="virtual-assistants-intents")
router.register(r"expressions", ExpressionViewSet, basename="virtual-assistants-expressions")
router.register(r"synonyms", SynonymViewSet, basename="virtual-assistants-synonyms")
router.register(r"regexs", RegexViewSet, basename="virtual-assistants-regexs")
router.register(r"actions", ActionViewSet, basename="virtual-assistants-actions")
router.register(r"responses", ResponseViewSet, basename="virtual-assistants-responses")
router.register(r"conversations", ConversationViewSet, basename="virtual-assistants-conversations")
router.register(r"models", NLUModelViewSet, basename="virtual-assistants-models")
router.register(r"stories", StoryViewSet, basename="virtual-assistants-stories")
router.register(r"rules", RuleViewSet, basename="virtual-assistants-rules")
router.register(r"utterances", UtteranceViewSet, basename="virtual-assistants-utterances")
router.register(r"nlu", NLUViewSet, basename="virtual-assistants-nlu")

bot_router = routers.NestedSimpleRouter(router, r"bots", lookup="bots")
bot_router.register(r"entities", EntityViewSet, basename="virtual-assistants-bot-entities")
bot_router.register(r"intents", IntentViewSet, basename="virtual-assistants-bot-intents")
bot_router.register(r"synonyms", SynonymViewSet, basename="virtual-assistants-bot-synonyms")
bot_router.register(r"regexs", RegexViewSet, basename="virtual-assistants-bot-regexs")
bot_router.register(r"actions", ActionViewSet, basename="virtual-assistants-bot-actions")
bot_router.register(r"responses", ResponseViewSet, basename="virtual-assistants-bot-responses")
bot_router.register(r"utterances", UtteranceViewSet, basename="virtual-assistants-bot-utterances")
bot_router.register(r"stories", StoryViewSet, basename="virtual-assistants-bot-stories")
bot_router.register(r"rules", RuleViewSet, basename="virtual-assistants-bot-rules")

public_router = routers.SimpleRouter(trailing_slash=False)
public_router.register(r"nlu", NLUPublicViewSet, basename="virtual-assistants-public-nlu")


urlpatterns = [
    path(r'api/v1/va/', include(router.urls)),
    path(r'api/v1/va/', include(bot_router.urls)),
    path(r'api/public/v1/va/', include(public_router.urls))
]
