from peewee import Model, CharField, BooleanField
from .db import db


class Category(Model):
    name = CharField()
    classification = BooleanField()

    class Meta:
        database = db
