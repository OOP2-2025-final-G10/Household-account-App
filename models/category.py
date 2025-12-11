from peewee import Model, CharField, ForeignKeyField
from .db import db

class Category(Model):
    name = CharField()
    classfication = ForeignKeyField(bool, backref='classification')

    class Meta:
        database = db