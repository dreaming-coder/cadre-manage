import json

__all__ = ["Config"]

with open("./config.json") as fp:
    Config = json.load(fp)


