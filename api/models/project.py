from django.db import models


class Project(models.Model):
    name = models.CharField(blank=False, max_length=250)
    description = models.CharField(blank=False, max_length=250)
    language = models.CharField(blank=False, max_length=250)
    stack = models.CharField(blank=False, max_length=250)
    github_link = models.CharField(blank=False, max_length=250)
    docs_link = models.CharField(blank=True, max_length=250)
