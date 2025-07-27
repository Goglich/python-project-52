from django.db import models
from django.db.models import ProtectedError

class Status(models.Model):
    name = models.CharField(max_length=255)
    time_create = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        if self.task_set.exists():
            raise ProtectedError(
                "Нельзя удалить статус, так как он связан с задачами.",
                self.task_set.all()
            )
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return self.name