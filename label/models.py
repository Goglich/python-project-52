from django.db import models
from django.db.models import ProtectedError

class Label(models.Model):
    name = models.CharField(max_length=255)
    time_create = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        if self.tasks.exists():
            raise ProtectedError(
                "Нельзя удалить метку, так как она связана с задачами.",
                self.tasks.all()
            )
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return self.name