from peewee import MySQLDatabase, Model
from os import getenv

conn = MySQLDatabase(
    getenv('DB_NAME'),
    user = getenv('DB_USERNAME'),
    password = getenv('DB_PASSWORD'),
    host = getenv('DB_HOST'),
    port = int(getenv('DB_PORT'))
)

class BaseModel(Model):
    class Meta:
        database = conn

conn.connect()