from django.db import models


class GameStatus(models.TextChoices):
    ONGOING = "Ongoing", "Ongoing"
    FINISHED = "Finished", "Finished"


class GameOrders(models.IntegerChoices):
    FIRST = 1
    SECOND = 2
