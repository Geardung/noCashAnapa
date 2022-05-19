from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase

try:
    db = PostgresqlDatabase(
        database="anapac",
        user="postgres",
        password="228485",
        host='localhost',
        port=5432)

except:
    db = PostgresqlExtDatabase(
        database='anapac',
        user='postgres',
        password="228485",
        host='localhost', 
        port=5432)

class BaseModel(Model):
    class Meta:
        database = db

class Users(BaseModel):
    
    phone = TextField(null=False)
    phone_ver = BooleanField(default=False)
    
