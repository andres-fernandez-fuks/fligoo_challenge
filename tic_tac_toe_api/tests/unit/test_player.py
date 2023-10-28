from django.test import TestCase
from django.db import IntegrityError

# Project
from tic_tac_toe_api.models import Game, Player


class TestPlayerRestrictionsTestCase(TestCase):
    def test_two_players_cannot_be_created_with_the_same_name_for_a_given_game(self):
        game = Game.objects.create()
        player_1 = Player.objects.create(name="Player 1", symbol="X", game_order=1)
        player_2 = Player.objects.create(name="Player 1", symbol="O", game_order=2)

        with self.assertRaises(IntegrityError):
            game.add_players([player_1, player_2])

    def test_two_players_cannot_be_created_with_the_same_symbol_for_a_given_game(self):
        game = Game.objects.create()
        player_1 = Player.objects.create(name="Player 1", symbol="X", game_order=1)
        player_2 = Player.objects.create(name="Player 2", symbol="X", game_order=2)

        with self.assertRaises(IntegrityError):
            game.add_players([player_1, player_2])
