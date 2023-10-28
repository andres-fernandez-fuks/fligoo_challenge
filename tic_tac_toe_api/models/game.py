from django.db import models
from typing import List

# Project
from tic_tac_toe_api.models.base_model import BaseModel
from tic_tac_toe_api.models.player import Player
from tic_tac_toe_api.utils.enums import GameStatus, GameOrder


class Game(BaseModel):
    COLUMNS = 3
    ROWS = 3

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
            self.board = [[None for _ in range(self.COLUMNS)] for _ in range(self.ROWS)]
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

    def is_valid_play(self, row: int, column: int) -> bool:
        if row < 0 or row >= self.ROWS:
            return False, "Row out of range."
        if column < 0 or column >= self.COLUMNS:
            return False, "Column out of range."
        current_cell_value = self.board[row][column]
        if current_cell_value is not None:
            return False, "Cell already played."
        return True, ""

    def _row_winner(self, symbol: str):
        pass

    def _column_winner(self, symbol: str):
        pass

    def _diagonal_winner(self, symbol: str):
        pass

    def _check_winner(self, player: Player):
        symbol = player.symbol
        if self._row_winner(symbol) or self._column_winner(symbol) or self._diagonal_winner(symbol):
            self.winner = player
            self.status = GameStatus.FINISHED
            self.save()

    def _update_next_turn(self, player: Player):
        if player == self.player_1:
            self.next_turn = self.player_2
        else:
            self.next_turn = self.player_1
        self.save()

    def submit_play(self, player: Player, row: int, column: int):
        self.board[row][column] = player.symbol
        self.movements_played += 1
        self._check_winner(player)
        self._update_next_turn(player)
