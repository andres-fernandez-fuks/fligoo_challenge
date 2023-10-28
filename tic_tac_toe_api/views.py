# Django rest framework
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

# Models
from tic_tac_toe_api.models import Game
from tic_tac_toe_api.serializers.game import GameCreationSerializer, GameModelSerializer


class GameViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = GameCreationSerializer
    queryset = Game.objects.all().order_by("-created_at")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        game_instance = serializer.create(serializer.validated_data)
        game_data = GameModelSerializer(game_instance).data
        return Response(game_data, status=status.HTTP_201_CREATED)
