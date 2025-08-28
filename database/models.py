from tortoise import fields
from tortoise.models import Model

class Editor(Model):
    id = fields.IntField(pk=True)
    discord_id = fields.CharField(max_length=50, unique=True)
    discord_username = fields.CharField(max_length=100)
    # a single channel manager can manage multiple creators
    creators = fields.ManyToManyField(
        "models.Creator",
        related_name="editors"
    )

class Creator(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    soft_deleted = fields.BooleanField(default=False)

    # Reverse relation (auto from related_name)
    managers: fields.ManyToManyRelation[Editor]