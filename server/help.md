## Set up environnement


python -m venv venv

venv\Scripts\activate    or    source venv/bin/activate

pip install fastapi uvicorn sqlalchemy psycopg2-binary "pydantic[email]" python-dotenv

pip freeze > requirements.txt



    FastAPI: Our web framework
    Uvicorn: An ASGI server to run our FastAPI application
    SQLAlchemy: An ORM for database interactions
    psycopg2-binary: PostgreSQL adapter for Python
    Pydantic: For data validation and settings management
    python-dotenv: To load environment variables from a .env file



## Run
python -m uvicorn main:app --reload

python -m uvicorn main:app


swagger : http://127.0.0.1:8000/docs
