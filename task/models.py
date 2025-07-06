from django.db import models
from django.contrib.auth.models import User
from status.models import Status

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(
        User, 
        on_delete=models.PROTECT,
        related_name='authored_tasks'
    )
    assignee = models.ForeignKey(
        User, 
        on_delete=models.PROTECT,
        null=True, 
        blank=True, 
        related_name='assigned_tasks'
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='task_set'
    )
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name