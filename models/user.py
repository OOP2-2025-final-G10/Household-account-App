from peewee import Model, CharField, AutoField
from .db import db

class User(Model):
    id = AutoField()
    name = CharField()

    class Meta:
        database = db
