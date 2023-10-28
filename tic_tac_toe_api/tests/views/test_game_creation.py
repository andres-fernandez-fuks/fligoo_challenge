from rest_framework.test import APITestCase


class GameCreationTestCase(APITestCase):
    def test_game_correct_creation(self):
        payload = {
            "players": [
                {"name": "Player 1"},
                {"name": "Player 2"},
            ],
            "starting_player": "Player 1",
        }
        url = "/games/"
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, 201)
        response_content = response.json()
        self.assertEqual(response_content["next_turn"], "Player 1")
        self.assertEqual(response_content["winner"], None)
        self.assertEqual(response_content["movements_played"], 0)
        players = response_content["players"]
        self.assertEqual(len(players), 2)
        player_1, player_2 = players
        self.assertEqual(player_1["name"], "Player 1")
        self.assertEqual(player_1["symbol"], "X")
        self.assertEqual(player_2["name"], "Player 2")
        self.assertEqual(player_2["symbol"], "O")

    def test_game_correct_creation_with_custom_symbols(self):
        PLAYER_1_SYMBOL = "A"
        PLAYER_2_SYMBOL = "B"
        payload = {
            "players": [
                {"name": "Player 1", "symbol": PLAYER_1_SYMBOL},
                {"name": "Player 2", "symbol": PLAYER_2_SYMBOL},
            ],
            "starting_player": "Player 1",
        }
        url = "/games/"
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, 201)
        response_content = response.json()
        self.assertEqual(response_content["next_turn"], "Player 1")
        self.assertEqual(response_content["winner"], None)
        self.assertEqual(response_content["movements_played"], 0)
        players = response_content["players"]
        self.assertEqual(len(players), 2)
        player_1, player_2 = players
        self.assertEqual(player_1["name"], "Player 1")
        self.assertEqual(player_1["symbol"], PLAYER_1_SYMBOL)
        self.assertEqual(player_2["name"], "Player 2")
        self.assertEqual(player_2["symbol"], PLAYER_2_SYMBOL)

    def test_game_creation_with_extra_players_throws_exception(self):
        payload = {
            "players": [
                {"name": "Player 1"},
                {"name": "Player 2"},
                {"name": "Player 3"},
            ],
            "starting_player": "Player 1",
        }
        url = "/games/"
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, 400)
        response_content = str(response.json())
        self.assertIn("A game must have exactly two players", response_content)

    def test_game_creation_with_incorrect_starting_player_throws_exception(self):
        payload = {
            "players": [
                {"name": "Player 1"},
                {"name": "Player 2"},
            ],
            "starting_player": "Player 3",
        }
        url = "/games/"
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, 400)
        response_content = str(response.json())
        self.assertIn("Starting player must be one of the players", response_content)

    def test_game_creation_with_same_player_names_throws_exception(self):
        payload = {
            "players": [
                {"name": "Player 1"},
                {"name": "Player 1"},
            ],
            "starting_player": "Player 1",
        }
        url = "/games/"
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, 400)
        response_content = str(response.json())
        self.assertIn("Players must have different names", response_content)

    def test_game_creation_with_same_player_symbols_throws_exception(self):
        payload = {
            "players": [
                {"name": "Player 1", "symbol": "X"},
                {"name": "Player 2", "symbol": "X"},
            ],
            "starting_player": "Player 1",
        }
        url = "/games/"
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, 400)
        response_content = str(response.json())
        self.assertIn("Players must have different symbols", response_content)
