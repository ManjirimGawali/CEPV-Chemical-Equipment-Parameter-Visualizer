from django.db import models

# Create your models here.
class Dataset(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    summary = models.JSONField()
    preview = models.JSONField(default=list)
    charts = models.JSONField(default=list)

    def __str__(self):
        return self.filename