from django.utils.translation import gettext as _
from common.constants.base import Const

class NLUDataTypes(Const):
    TEXT = "text"
    BOOL = "bool"
    CATEGORICAL = "categorical"
    FLOAT = "float"
    LIST = "list"
    UNFEATURIZED = "unfeaturized"

    CHOICES = (
        (TEXT, _("Text")),
        (BOOL, _("Boolean")),
        (CATEGORICAL, _("Categorical")),
        (FLOAT, _("Float")),
        (LIST, _("List")),
        (UNFEATURIZED, _("Unfeaturized"))
    )