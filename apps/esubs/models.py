from django.db import models


class Subscriptions(models.Model):
    email = models.EmailField()
    added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email