from django.db import models
from django.conf import settings


class Score(models.Model):
    score = models.IntegerField(blank=False, default=0)
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="scores", on_delete=models.CASCADE
    )
    game = models.ForeignKey(
        "GameType", related_name="scores", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["-score"]
