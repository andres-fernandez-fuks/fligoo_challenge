from rest_framework import serializers

# Project
from tic_tac_toe_api.models import Player
from tic_tac_toe_api.utils.enums import GameOrder, GameSymbols


class PlayerBasicCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ("name", "symbol", "game_order")
        extra_kwargs = {"symbol": {"required": False}, "game_order": {"required": False, "write_only": True}}

    def create(self, validated_data):
        game_order = validated_data.get("game_order")
        if "symbol" not in validated_data:
            symbol = GameSymbols._X if game_order == GameOrder.FIRST else GameSymbols._O
            validated_data["symbol"] = symbol
        return Player.objects.create(**validated_data)


class PlayerBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ("name", "symbol")
