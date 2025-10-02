from .evaluation_template_status import EvaluationTemplateStatus
from .leave_paid_type import LeavePaidType
from .leave_request_status import LeaveRequestStatus

client_constants = {
    "leave_paid_types": [{"value": x, "description": y} for x, y in LeavePaidType.CHOICES],
    "leave_request_statuses": [{"value": x, "description": y} for x, y in LeaveRequestStatus.CHOICES],
    "evaluation_template_statuses": [{"value": x, "description": y} for x, y in EvaluationTemplateStatus.CHOICES]
}