import functools
import json
from datetime import date, datetime, time

from peewee import Model


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, time):
            return obj.strftime('%H:%M:%S')
        elif isinstance(obj, Model):
            return obj.json()
        else:
            return json.JSONEncoder.default(self, obj)


json_dumps = functools.partial(json.dumps, cls=ComplexEncoder, ensure_ascii=False)
