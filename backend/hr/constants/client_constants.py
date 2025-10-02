from . import LeavePaidType, LeaveRequestStatus, EvaluationTemplateStatus

client_constants = {
    "leave_paid_types": [{"value": x, "description": y} for x, y in LeavePaidType.CHOICES],
    "leave_request_statuses": [{"value": x, "description": y} for x, y in LeaveRequestStatus.CHOICES],
    "evaluation_template_statuses": [{"value": x, "description": y} for x, y in EvaluationTemplateStatus.CHOICES]
}