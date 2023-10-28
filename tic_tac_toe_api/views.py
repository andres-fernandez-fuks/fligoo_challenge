# Django rest framework
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

# Models
from tic_tac_toe_api.models import Game
from tic_tac_toe_api.serializers.game import GameCreationSerializer, GameModelSerializer, NewPlaySerializer


class GameViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = GameCreationSerializer
    queryset = Game.objects.all().order_by("-created_at")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        game = serializer.create(serializer.validated_data)
        game_data = GameModelSerializer(game).data
        return Response(game_data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path="submit-play")
    def submit_play(self, request):
        serializer = NewPlaySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        game: Game = serializer.validated_data.pop("game")
        game.submit_play(**serializer.validated_data)
        game_data = GameModelSerializer(game).data
        return Response(game_data)
