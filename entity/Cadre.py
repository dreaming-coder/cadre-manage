from peewee import Model, TextField, DateField, IntegerField

from db import table_name

__all__ = [
    "Cadre"
]


@table_name("cadre")
class Cadre(Model):
    name = TextField()
    birthdate = DateField(formats="%Y-%m-%d")
    age = IntegerField()
