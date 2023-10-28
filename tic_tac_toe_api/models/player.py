from django.db import models

# Project
from tic_tac_toe_api.models.base_model import BaseModel
from tic_tac_toe_api.utils.enums import GameOrders


class Player(BaseModel):
    name = models.CharField(max_length=255, help_text="Player name.")
    symbol = models.CharField(max_length=1, help_text="Player symbol for a given game")
    game = models.ForeignKey(
        "Game",
        on_delete=models.CASCADE,
        related_name="players",
        null=True,  # allows for player creation before game creation (in Serializer, maybe)
        help_text="Game the player is playing.",
    )
    game_order = models.PositiveSmallIntegerField(
        choices=GameOrders.choices,
        help_text="Order of the player in the game."
    )

    unique_together = [["name", "game"], ["symbol", "game"]]
    # Two players cannot have the same name or symbol in the same game

    def __str__(self):
        return self.name
