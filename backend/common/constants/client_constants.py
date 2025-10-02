from . import DataType, PaperValidateStatus, IndentityPaperType, PublishingStatus

client_constants = {
    "data_types": [{"value": x, "description": y} for x, y in DataType.CHOICES],
    "paper_validate_statuses": [{"value": x, "description": y} for x, y in PaperValidateStatus.CHOICES],
    "indentity_paper_types": [{"value": x, "description": y} for x, y in IndentityPaperType.CHOICES],
    "publishing_statuses": [{"value": x, "description": y} for x, y in PublishingStatus.CHOICES]
}