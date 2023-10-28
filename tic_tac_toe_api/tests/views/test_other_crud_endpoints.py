from rest_framework.test import APITestCase

# Project
from tic_tac_toe_api.models.game import Game


class GameCRUDEndpoints(APITestCase):
    def setUp(self):
        response = self.create_game()
        self.game_id = response.json()["id"]
        self.game = Game.objects.get(id=self.game_id)

    def create_game(self):
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
        return response

    def test_retrieve_game(self):
        url = f"/games/{self.game_id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_content = response.json()
        self.assertEqual(response_content["id"], self.game_id)
        self.assertEqual(response_content["next_turn"], self.game.next_turn.name)
        self.assertEqual(response_content["movements_played"], self.game.movements_played)
        self.assertEqual(response_content["board"], self.game.board)
        self.assertEqual(response_content["winner"], self.game.winner.name if self.game.winner else None)

    def test_list_games(self):
        TOTAL_GAMES = 3
        for _ in range(TOTAL_GAMES - 1):  # one is already created
            self.create_game()

        url = "/games/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_content = response.json()
        self.assertEqual(len(response_content), TOTAL_GAMES)

    def test_delete_game(self):
        url = f"/games/{self.game_id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Game.objects.count(), 0)
