
# Weight-Manager Front End

## Set up environnement
```
python -m venv venv
```

## Source environnement
venv\Scripts\activate    or    source venv/bin/activate

## Install packages
```
pip install fastapi uvicorn sqlalchemy psycopg2-binary "pydantic[email]" python-dotenv pydantic-collections
```

## Requirement file for Docker
```
pip freeze > requirements.txt
```

>FastAPI: Our web framework
>Uvicorn: An ASGI server to run our FastAPI application
>SQLAlchemy: An ORM for database interactions
>psycopg2-binary: PostgreSQL adapter for Python
>Pydantic: For data validation and settings management
>pydantic-collections: Manage collections
>python-dotenv: To load environment variables from a .env file

## Run server
```
python -m uvicorn main:app --reload
```

or

```
python -m uvicorn main:app
```

## Acces to API Swagger
swagger : http://127.0.0.1:8000/docs


## Build container

Dockerfile:
```Docker
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build:
```
docker build -t weight-manager-api .
```

Start:
```
docker run -d -p 8000:8000 weight-manager-api
```

