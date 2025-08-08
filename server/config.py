from dotenv import load_dotenv
import os
import redis
from datetime import timedelta


load_dotenv()

class ApplicationConfig():
    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = r"sqlite:///./db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'sharmachinu2003@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)

