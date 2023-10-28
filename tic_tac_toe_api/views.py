# Django rest framework
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema, swagger_serializer_method
from rest_framework import status

# Project
import tic_tac_toe_api.utils.documentation as doc
from tic_tac_toe_api.models import Game
from tic_tac_toe_api.serializers.game import GameCreationSerializer, GameModelSerializer, NewPlaySerializer


class GameViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = GameModelSerializer
    queryset = Game.objects.all().order_by("-created_at")

    @swagger_auto_schema(
        request_body=GameCreationSerializer,
        responses=doc.game_creation_responses,
        operation_description="Retrieves the law projects of a legislator",
    )
    def create(self, request, *args, **kwargs):
        serializer = GameCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        game = serializer.create(serializer.validated_data)
        game_data = GameModelSerializer(game).data
        return Response(game_data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        method="post",
        request_body=NewPlaySerializer,
        responses=doc.game_creation_responses,
        operation_description="Retrieves the law projects of a legislator",
    )
    @action(detail=False, methods=["post"], url_path="submit-play")
    def submit_play(self, request):
        serializer = NewPlaySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        game: Game = serializer.validated_data.pop("game")
        game.submit_play(**serializer.validated_data)
        game_data = GameModelSerializer(game).data
        return Response(game_data)
