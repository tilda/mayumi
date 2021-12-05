import orm
from databases import Database

instance = Database("sqlite:///mayumi.sqlite")
registry = orm.ModelRegistry(database=instance)

class User(orm.Model):
    tablename = "users"
    registry = registry
    fields = {
        "twitchID": orm.Integer(primary_key=True),
        "osuID": orm.Integer(),
        "reqsEnabled": orm.Boolean(default=False),
        "setupComplete": orm.Boolean(default=False)
    }