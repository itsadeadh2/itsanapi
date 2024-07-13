from django.db import models


class GameType(models.Model):
    name = models.CharField(blank=False, max_length=250, unique=True)
    slug = models.SlugField(max_length=250)
