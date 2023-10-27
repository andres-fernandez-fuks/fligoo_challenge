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