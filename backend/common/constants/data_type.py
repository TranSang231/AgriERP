from django.utils.translation import gettext as _
from .base import Const

class DataType(Const):
    CHAR_FIELD = "CharField"
    TEXT_FIELD = "TextField"
    BOOLEAN_FIELD = "BooleanField"
    INTEGER_FIELD = "IntegerField"
    BIG_INTEGER_FIELD = "BigIntegerField"
    FLOAT_FIELD = "FloatField"
    DATE_FIELD = "DateField"
    DATE_TIME_FIELD = "DateTimeField"
    CHOICES = (
        (CHAR_FIELD, _("Char")),
        (TEXT_FIELD, _("Text")),
        (BOOLEAN_FIELD, _("Boolean")),
        (INTEGER_FIELD, _("Integer")),
        (BIG_INTEGER_FIELD, _("Big Integer")),
        (FLOAT_FIELD, _("Float")),
        (DATE_FIELD, _("Date")),
        (DATE_TIME_FIELD, _("Date and Time"))
    )