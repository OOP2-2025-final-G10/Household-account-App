from peewee import Model, ForeignKeyField, DateTimeField, IntegerField, TextField
from .db import db
from .user import User
from .category import Category
import datetime as dt

class Record(Model):
    user = ForeignKeyField(User, backref='records')
    category = ForeignKeyField(Category, backref='records')
    price = IntegerField()
    date = DateTimeField(default=dt.datetime.now)
    memo = TextField(null=True)

    class Meta:
        database = db
