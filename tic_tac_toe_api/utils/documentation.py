from drf_yasg import openapi
from rest_framework import status

# Project
from tic_tac_toe_api.serializers.game import GameModelSerializer

game_creation_response = openapi.Response("Game creation response", GameModelSerializer)
game_creation_responses = {status.HTTP_201_CREATED: game_creation_response}


submit_play_response = openapi.Response("Submit play response", GameModelSerializer)
submit_play_responses = {status.HTTP_200_OK: submit_play_response}
