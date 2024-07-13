from django.db import models


class Score(models.Model):
    score = models.IntegerField(blank=False, default=0)
    player = models.ForeignKey(
        "auth.User", related_name="scores", on_delete=models.CASCADE
    )
    game = models.ForeignKey(
        "GameType", related_name="scores", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["-score"]
