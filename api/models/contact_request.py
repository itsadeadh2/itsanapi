from django.db import models


class ContactRequest(models.Model):
    email = models.EmailField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
