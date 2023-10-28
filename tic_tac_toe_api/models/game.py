from django.db import models
from typing import List

# Project
from tic_tac_toe_api.models.base_model import BaseModel
from tic_tac_toe_api.models.player import Player
from tic_tac_toe_api.utils.enums import GameStatus, GameOrder


class Game(BaseModel):
    next_turn = models.ForeignKey(
        "Player",
        on_delete=models.CASCADE,
        related_name="games",
        help_text="Player who will play next.",
        null=True,  # players are added after game creation
    )
    winner = models.ForeignKey(
        "Player",
        on_delete=models.CASCADE,
        related_name="won_games",
        null=True,
        help_text="Player who won the game.",
    )
    board = models.JSONField()  # Probably a class on its own later
    status = models.CharField(choices=GameStatus.choices, max_length=20, default=GameStatus.ONGOING)
    movements_played = models.PositiveSmallIntegerField(default=0)

    def set_players_game(self, players: List[Player]):
        player_1, player_2 = sorted(players, key=lambda p: p.game_order)
        player_1.game = self
        player_2.game = self
        player_1.save()
        player_2.save()

    def save(self, *args, **kwargs):
        is_creation = not self.pk
        if is_creation:  # On game creation only
            self.board = [[None for _ in range(3)] for _ in range(3)]
        super().save(*args, **kwargs)

    def add_players(self, players: List[Player]):
        self.set_players_game(players)
        self.next_turn = self.player_1
        self.save()

    @property
    def player_1(self) -> Player:
        return self.players.get(game_order=GameOrder.FIRST)

    @property
    def player_2(self) -> Player:
        return self.players.get(game_order=GameOrder.SECOND)
