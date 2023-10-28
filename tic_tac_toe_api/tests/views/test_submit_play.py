from rest_framework.test import APITestCase

# Project
from tic_tac_toe_api.models.game import Game


class GameCreationTestCase(APITestCase):
    def setUp(self):
        self.player_1_name = "Player 1"
        self.player_2_name = "Player 2"
        payload = {
            "players": [
                {"name": self.player_1_name},
                {"name": self.player_2_name},
            ],
            "starting_player": self.player_1_name,
        }
        url = "/games/"
        response = self.client.post(url, payload, format="json")
        self.game_id = response.json()["id"]

    def submit_play(self, player_name: str, row: int, column: int):
        payload = {
            "game_id": self.game_id,
            "player": player_name,
            "row": row,
            "column": column,
        }
        url = "/games/submit-play/"
        response = self.client.post(url, payload, format="json")
        return response

    def test_basic_play_submition(self):
        VALID_ROW = 0
        VALID_COLUMN = 0
        player = self.player_1_name
        response = self.submit_play(player, VALID_ROW, VALID_COLUMN)
        self.assertEqual(response.status_code, 200)
        response_content = response.json()
        self.assertEqual(response_content["next_turn"], self.player_2_name)
        self.assertEqual(response_content["movements_played"], 1)
        board = response_content["board"]
        self.assertEqual(board[VALID_ROW][VALID_COLUMN], "X")

    def test_second_play(self):
        FIRST_ROW = FIRST_COLUMN = 0
        first_player = self.player_1_name
        self.submit_play(first_player, FIRST_ROW, FIRST_COLUMN)
        SECOND_ROW = SECOND_COLUMN = 1
        second_player = self.player_2_name
        response = self.submit_play(second_player, SECOND_ROW, SECOND_COLUMN)
        response_content = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content["next_turn"], self.player_1_name)
        self.assertEqual(response_content["movements_played"], 2)
        board = response_content["board"]
        self.assertEqual(board[FIRST_ROW][FIRST_COLUMN], "X")
        self.assertEqual(board[SECOND_ROW][SECOND_COLUMN], "O")

    def test_play_out_of_range_column_throws_exception(self):
        VALID_ROW = 0
        INVALID_COLUMN = 3
        player = self.player_1_name
        response = self.submit_play(player, VALID_ROW, INVALID_COLUMN)
        self.assertEqual(response.status_code, 400)
        response_content = str(response.json())
        self.assertIn("Column out of range.", response_content)

    def test_play_out_of_range_row_throws_exception(self):
        INVALID_ROW = 3
        VALID_COLUMN = 0
        player = self.player_1_name
        response = self.submit_play(player, INVALID_ROW, VALID_COLUMN)
        self.assertEqual(response.status_code, 400)
        response_content = str(response.json())
        self.assertIn("Row out of range.", response_content)

    def test_play_by_incorrect_player_throws_exception(self):
        VALID_ROW = 0
        VALID_COLUMN = 0
        player = self.player_2_name
        response = self.submit_play(player, VALID_ROW, VALID_COLUMN)
        self.assertEqual(response.status_code, 400)
        response_content = str(response.json())
        self.assertIn("It's not this player's turn.", response_content)

    def test_play_in_game_with_winner_throws_exception(self):
        player = self.player_1_name
        VALID_ROW = VALID_COLUMN = 0
        game = Game.objects.get(id=self.game_id)
        game.winner = game.player_1
        game.save()
        response = self.submit_play(player, 0, 2)
        self.assertEqual(response.status_code, 400)
        response_content = str(response.json())
        self.assertIn("Game is already finished.", response_content)
