# fligoo_challenge

## Descripción

Challenge para la empresa Fligoo.
 
## Comentarios

* La aplicación no se puede llamar "tic_tac_toe" porque existe un módulo en Python con ese nombre, por eso "tic_tac_toe_api".


## Ejecución

Docker build:

```
docker compose -f local.yml build
```

Docker run:

Se recomienda ejecutar el script run.sh, donde se pueden setear fácilmente puertos externos:

```
chmod +x run.sh
./run.sh
```

De lo contrario, se puede ejecutar simplemente:

```
docker compose -f local.yml run --rm --service-ports django.tic_tac_toe_api
```

## Decisiones

* De acuerdo a los requisitos, entiendo que un Player debería existir sólo dentro de Game. No hay historial para los jugadores, ni otras cuestiones que llevarían a que Player existiera fuera de un Game. Por eso, defino la relación de la manera que se muestra en models: un Player tiene un Game, y no viceversa.

* Este cambio me llevó algo de tiempo, hubiera sido más simple tener player_1 y player_2 dentro de Game, pero me pareció claro que no era la idea del enunciado. Por otro lado, la adición de los jugadores al juego no puede hacerse en la creación, por limitaciones de Django, por lo que quedó en un método aparte, y llevó a permitir algunos campos en null=True (Person->game y Game->next_move). También podía overridear el delete de Game para que borre los players, pero me pareció mejor esta alternativa.

* Next move podría ser simplemente un booleano (0,1) o int que sirviera para moverse en el array de jugadores (1 o 2). Sin embargo, lo defino como una foreign key a Player que es simplemente un id y funciona de forma similar.

* Agrego validación de que nombres y símbolos de jugadores no sean iguales para el mismo juego tanto a nivel de serializer como de modelo. Si bien obviamente esto implica una redundancia en la validación, entiendo que el modelo debe verificarlo y es una validación muy simple.