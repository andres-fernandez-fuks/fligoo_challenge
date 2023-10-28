from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        "created at", auto_now_add=True, help_text="Date time on which the object was created."
    )
    updated_at = models.DateTimeField(
        "updated at", auto_now=True, help_text="Date time on which the object was last modified."
    )
    id = models.AutoField(primary_key=True, editable=False, serialize=False)
