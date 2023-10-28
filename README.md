# fligoo_challenge

## Descripción

Challenge para la empresa Fligoo.
 
## Comentarios

* La aplicación no se puede llamar "tic_tac_toe" porque existe un módulo en Python con ese nombre, por eso "tic_tac_toe_api".


## Ejecución

Renombrar los archivos:

- .envs/django_sample -> .envs/django 
-.envs/postgres_sample -> .envs/postgres

y setear las variables de entorno correspondientes en postgres.

Docker build:

Se puede hacer el build utilizando el script run.sh de la base del proyecto, de esta forma:

```
chmod +x run.sh (sólo la primera vez)
./run.sh --build
```

También se puede hacer el build directamente con docker compose:

```
docker compose -f local.yml build
```

Docker run:

Se recomienda ejecutar el script run.sh, donde se pueden setear fácilmente puertos externos:

```
chmod +x run.sh (sólo la primera vez)
./run.sh
```

De lo contrario, se puede ejecutar simplemente:

```
docker compose -f local.yml run --rm --service-ports django.tic_tac_toe_api
docker exec -it ${NOMBRE_DEL_CONTENEDOR} bash
```


## Decisiones

* Tiempo estimado de desarrollo: 5 horas.

* Faltante: falta la lógica de verificación de un ganador. Dejé las funciones que verificarían eso vacías, pero es bastante trivial cómo se buscaría el ganador en el tablero. También, en ese caso, debería hacer las pruebas unitarias asociadas.

* Había pensado en que Board fuera una clase en sí mismo, pero no me pareció que fuera necesario. El tablero es simplemente un array de 9 posiciones, y no tiene lógica asociada, aunque se podría delegar cierta lógica de Game al Board eventualmente.

* El campo game_order quedó en la documentación de swagger del endpoint de creación de Game, aunque no es un campo que debería pasarse. No estoy seguro de la mejor forma de solucionarlo, pero en el peor de los casos se pueden usar dos serializers distintos para la validación y la creación de un Player en un Game.

* De acuerdo a los requisitos, entiendo que un Player debería existir sólo dentro de Game. No hay historial para los jugadores, ni otras cuestiones que llevarían a que Player existiera fuera de un Game. Por eso, defino la relación de la manera que se muestra en models: un Player tiene un Game, y no viceversa.

* Este cambio me llevó algo de tiempo, hubiera sido más simple tener player_1 y player_2 dentro de Game, pero me pareció claro que no era la idea del enunciado. Por otro lado, la adición de los jugadores al juego no puede hacerse en la creación, por limitaciones de Django, por lo que quedó en un método aparte, y llevó a permitir algunos campos en null=True (Person->game y Game->next_move). También podía overridear el delete de Game para que borre los players, pero me pareció mejor esta alternativa.

* Next move podría ser simplemente un booleano (0,1) o int que sirviera para moverse en el array de jugadores (1 o 2). Sin embargo, lo defino como una foreign key a Player que es simplemente un id y funciona de forma similar.

* Agrego validación de que nombres y símbolos de jugadores no sean iguales para el mismo juego tanto a nivel de serializer como de modelo. Si bien obviamente esto implica una redundancia en la validación, entiendo que el modelo debe verificarlo y es una validación muy simple.
 

 ## Preguntas

* **How would you let the players choose their symbols instead of using X and O?**\
Está hecho en la aplicación.
* **Let the players choose who goes first instead of always choosing the first player in the list.**\
Está hecho en la aplicación, creí que era parte del enunciado.
* **How can the API validate and handle malformed inputs or invalid data?**\
Queda en parte en la validación propia de los serializers de Django y en otra, lo valido manualmente, como se puede ver.
* **How can the API validate and handle malformed inputs or invalid data? Consider the case where the same player tries to play twice in a row, or a player attempts to make a move to a finished game.**\
Misma respuesta, agrego validación de algunos escenarios como los mencionados, y Django agrega validaciones propias.
* **How would you extend the endpoint to return only finished or unfinished games?**\
Con filtros. En el caso de Django, tiene filtros integrados muy fáciles de usar. Yo creé un atributo GameStatus que se podría usar para ese filtro, aunque no lo uso realmente hasta ahora. Obviamente, el filtro también se podría usar con el atributo winner (si es o no None). El filtro debería venir como parámetro de la request a "/games/". El filtro se aplicaría a la query de la Base de Datos.
* **What would happen if you had millions of stored games? Is there something you can do to avoid returning all of them at once?**\
A través de la paginación de la respuesta. Se debería recibir un parámetro de page_size en la request inicial, y luego con los resultados se devolvería también la url de la siguiente página, hasta que se terminen los resultados. 
 * **How would you handle the case where the ID is invalid?**\
Creo que un 404 es la mejor opción.
* **Imagine the data needed when listing games is different from the data needed when retrieving a game. How would you implement that?**\
Los serializers de Django, o la clase equivalente en otros frameworks, se debería encargar de definir qué data mostrar en cada caso.
* **How would you handle the case where the ID is invalid?**\
De la misma forma, con un 404.
* **And what about trying to delete a game that’s already deleted?**\
Las requests de DELETE son idempotentes (varias ejecuciones de la misma request tienen el mismo resultado), por lo que no se debería levantar un error en caso de que se hiciera varias veces la request. La primera vez, se eliminará el Game de la base de datos. Las sucesivas, el juego ya estará eliminado inicialmente, por lo que no se hará nada.


 