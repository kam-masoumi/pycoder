from peewee import *

from models.model_manager import DATA_BASE


class Font(Model):
    type = CharField(max_length=200, default="zar")
    size = FloatField(default=10.0)
    code = CharField(max_length=10, default="True", unique=True)

    class Meta:
        database = DATA_BASE
