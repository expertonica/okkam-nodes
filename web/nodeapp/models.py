from django.db import models
from django.db.models import JSONField

# Create your models here.

class UrlWc(models.Model):
    url = models.CharField(max_length=2048, db_index=True)
    company_id = models.IntegerField(db_index=True)
    company_url = models.CharField(max_length=128)
    word_counter = JSONField()

