from typing import List
from rest_framework import serializers
from tic_tac_toe_api.models.game import Game
from tic_tac_toe_api.models.player import Player

from tic_tac_toe_api.serializers.player import PlayerBasicCreationSerializer, PlayerBasicInfoSerializer
from tic_tac_toe_api.utils.enums import GameOrder


class GameModelSerializer(serializers.ModelSerializer):
    players = PlayerBasicInfoSerializer(many=True)
    next_turn = serializers.SerializerMethodField()
    winner = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ("id", "players", "next_turn", "board", "winner", "movements_played")

    def get_next_turn(self, game: Game):
        return game.next_turn.name

    def get_winner(self, game: Game):
        return game.winner.name if game.winner else None


class GameCreationSerializer(serializers.Serializer):
    players = PlayerBasicCreationSerializer(many=True)
    starting_player = serializers.CharField()

    def _validate_amount_of_players(self, players_info: List[dict]):
        if len(players_info) != 2:
            raise serializers.ValidationError("A game must have exactly two players.")

    def _validate_player_names(self, players_info: List[dict]):
        player_1_name = players_info[0]["name"]
        player_2_name = players_info[1]["name"]
        if player_1_name == player_2_name:
            raise serializers.ValidationError("Players must have different names.")

    def _validate_player_simbols(self, players_info: List[dict]):
        player_1_symbol = players_info[0].get("symbol")
        player_2_symbol = players_info[1].get("symbol")
        if not player_1_symbol or not player_2_symbol:
            return  # symbols are optional
        if player_1_symbol == player_2_symbol:
            raise serializers.ValidationError("Players must have different symbols.")

    def _validate_starting_player(self, players_info: List[dict], starting_player: str):
        player_1_name = players_info[0]["name"]
        player_2_name = players_info[1]["name"]
        if starting_player not in [player_1_name, player_2_name]:
            raise serializers.ValidationError("Starting player must be one of the players.")

    def validate(self, data):
        super().validate(data)
        players_info = data["players"]
        starting_player = data["starting_player"]
        self._validate_amount_of_players(players_info)
        self._validate_player_names(players_info)
        self._validate_player_simbols(players_info)
        self._validate_starting_player(players_info, starting_player)
        return data

    def _sort_players(self, players_info: List[dict], starting_player: str):
        # In addition to sorting, it adds the field "game_order" to the players
        player_1_info, player_2_info = players_info
        if player_1_info["name"] == starting_player:
            players_info[0]["game_order"] = GameOrder.FIRST
            players_info[1]["game_order"] = GameOrder.SECOND
            return [player_1_info, player_2_info]
        elif player_2_info["name"] == starting_player:  # unnecesary, but the variable is already there
            players_info[0]["game_order"] = GameOrder.SECOND
            players_info[1]["game_order"] = GameOrder.FIRST
            return [player_2_info, player_1_info]

    def create(self, validated_data):
        players_info = validated_data["players"]
        starting_player = validated_data["starting_player"]
        sorted_players: List[dict] = self._sort_players(players_info, starting_player)
        players = PlayerBasicCreationSerializer(data=sorted_players, many=True).create(sorted_players)
        game = Game.objects.create()
        game.add_players(players)
        return game
