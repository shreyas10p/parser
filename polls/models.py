from django.db import models

# Create your models here.

class PdfData(models.Model):
    order_id = models.CharField(max_length=255, unique=True, primary_key=True)
    data = models.TextField()
