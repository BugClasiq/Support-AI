import os
from dotenv import load_dotenv


load_dotenv()


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY"
    )


    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://"
        + os.getenv("DB_USER")
        + ":"
        + os.getenv("DB_PASSWORD")
        + "@"
        + os.getenv("DB_HOST")
        + ":"
        + os.getenv("DB_PORT")
        + "/"
        + os.getenv("DB_NAME")
    )


    SQLALCHEMY_TRACK_MODIFICATIONS = False


    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY"
    )


    OPENAI_API_KEY = os.getenv(
        "OPENAI_API_KEY"
    )


    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY"
    )


    LLM_PROVIDER = os.getenv(
        "LLM_PROVIDER"
    )