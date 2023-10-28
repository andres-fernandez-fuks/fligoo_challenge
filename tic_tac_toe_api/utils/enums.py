from django.db import models


class GameStatus(models.TextChoices):
    ONGOING = "Ongoing", "Ongoing"
    FINISHED = "Finished", "Finished"


class GameOrder(models.IntegerChoices):
    FIRST = 1
    SECOND = 2


class GameSymbols(models.TextChoices):
    _X = "X", "X"
    _O = "O", "O"
