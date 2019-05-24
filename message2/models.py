from django.db import models

# Create your models here.

class Message(models.Model):
    mid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    content = models.CharField(max_length=500, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    author = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'message'
