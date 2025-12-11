from peewee import Model, ForeignKeyField, DateTimeField
from .db import db
from .user import User
from .category import Category
import datetime as dt

class Record(Model):
    user = ForeignKeyField(User, backref='orders')
    category = ForeignKeyField(Category, backref='category')
    price = ForeignKeyField(int, backref='price')
    date = DateTimeField(default=dt.datetime.now)
    memo = ForeignKeyField(str, backref='memo', null=True)

    class Meta:
        database = db
