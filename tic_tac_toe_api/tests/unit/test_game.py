from django.test import TestCase
from typing import List

# Project
from tic_tac_toe_api.models import Game, Player
from tic_tac_toe_api.utils.enums import GameStatus


class GameTestCase(TestCase):
    def assert_board_is_empty(self, board: List[List]):
        for row in board:
            for cell in row:
                self.assertIsNone(cell)

    def test_game_creation(self):
        player_1 = Player.objects.create(name="Player 1", symbol="X", game_order=1)
        player_2 = Player.objects.create(name="Player 2", symbol="O", game_order=2)
        players = [player_1, player_2]
        game = Game.objects.create()
        game.add_players(players)
        self.assertEqual(game.player_1, player_1)
        self.assertEqual(game.player_2, player_2)
        self.assertEqual(game.next_turn, player_1)
        self.assertIsNotNone(game.board)
        self.assert_board_is_empty(game.board)
        self.assertEqual(game.status, GameStatus.ONGOING)

    def test_players_are_deleted_when_game_is_deleted(self):
        player_1 = Player.objects.create(name="Player 1", symbol="X", game_order=1)
        player_2 = Player.objects.create(name="Player 2", symbol="O", game_order=2)
        players = [player_1, player_2]
        game = Game.objects.create()
        game.add_players(players)
        game.delete()
        self.assertEqual(Player.objects.count(), 0)
