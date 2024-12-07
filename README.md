# TwitSnap-User-API
Microservicio de usuario para TwitSnap, con funcionalidades de registro con mail y contrasena o con Google,
seguimiento, baneo, y CRUD de usuarios. 
Desarrollado en `Python` y `FastAPI`, con base de datos en `Neo4j`.

## Ejecucion con Docker
```
docker build -t <nombre_imagen> .
```
```
docker run -d -p 8000:8000 <nombre_imagen>
```
## Ejecucion local
### Pre-requisitos
- Python 3.10 o superior
### Creacion de entorno virtual
```
python3 -m venv venv
source venv/bin/activate
```
### Instalacion de dependencias
```
pip install -r requirements.txt
```
### Ejecucion
```
python3 src/main.py
```

## Documentacion
La documentacion de la API se encuentra en la ruta `/docs` del servidor.
[API Docs](https://twitsnap-user-api-af1u.onrender.com/docs)
## Ejecucion de Tests
```
pytest --cov=src --cov-report=term 
```