from django.db import models
from django.conf import settings


class HangmanGame(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = "GAME_IN_PROGRESS", "GAME_IN_PROGRESS"
        WON = "GAME_WON", "GAME_WON"
        LOST = "GAME_LOST", "GAME_LOST"

    solution = models.CharField(blank=False, max_length=250)
    attempts_left = models.IntegerField(blank=False, default=6)
    status = models.CharField(choices=Status.choices, max_length=100)
    masked_word = models.CharField(blank=False, max_length=250)
    game = models.ForeignKey("GameType", on_delete=models.CASCADE)
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="hangman_games", on_delete=models.CASCADE
    )

    @staticmethod
    def get_masked_text(text):
        return "".join(["_" for x in text])

    def update_mask_for_letter(self, letter):
        current_mask = list(self.masked_word)
        for idx, letter_in_solution in enumerate(self.solution):
            if letter.lower() == letter_in_solution.lower():
                current_mask[idx] = letter
        self.masked_word = "".join(current_mask)

    def is_guess_correct(self, letter):
        return letter.lower() in self.solution.lower()

    def handle_guess(self, letter):
        success = self.is_guess_correct(letter)
        if success:
            self.update_mask_for_letter(letter)
            is_solution_complete = self.solution.lower() == self.masked_word.lower()
            if is_solution_complete:
                self.status = self.Status.WON
        else:
            self.attempts_left -= 1
            if self.attempts_left == 0:
                self.status = self.Status.LOST
