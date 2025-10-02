from .timestamped import TimeStampedModel
from .user_audit_model import UserAuditModel

class AuditModel(TimeStampedModel, UserAuditModel):
    """To path when the record was created and last modified"""

    class Meta:
        abstract = True