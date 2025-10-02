from django.db import models
from base.models.timestamped import TimeStampedModel
from .long_content import LongContent


# def file_name(instance, filename):
#     # end_path = str(instance.id) + '.' + filename.split('.')[-1]
#     # final_path = "/".join(
#     #     ['courses', str(instance.lesson.chapter.course.id), 'chapters', str(instance.lesson.chapter.id), 'lessons',
#     #      str(instance.lesson.id), 'responser', str(instance.responser.id), str(end_path)])
#
#     return final_path

def attachment_path(instance, filename):
    return instance.path


class Attachment(TimeStampedModel):
    path = models.CharField(default=None, null=True, max_length=255)
    file = models.FileField(
        upload_to=attachment_path, max_length=255, blank=True, null=True
    )
    mine_type = models.CharField(max_length=255)
    long_content = models.ForeignKey(LongContent, null=True, blank=True, on_delete=models.CASCADE, related_name="attachments")
    original_name = models.CharField(max_length=255)
    length = models.IntegerField(default=0)

    class Meta:
        db_table = "long_content_attachments"
        ordering = ["-created_at"]
