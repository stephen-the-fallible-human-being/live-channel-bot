from tortoise import fields
from tortoise.models import Model

class GuildConfig(Model):
    id = fields.IntField(pk=True)
    guild_id = fields.CharField(max_length=50)
    thumbnail_designer_role_id = fields.CharField(max_length=50, null=True)
    editor_role_id = fields.CharField(max_length=50, null=True)

class Creator(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    soft_deleted = fields.BooleanField(default=False)

    class Meta:
        table = "creators"

class Designer(Model):
    id = fields.IntField(pk=True)
    discord_id = fields.CharField(max_length=50, unique=True)
    discord_username = fields.CharField(max_length=100)
    soft_deleted = fields.BooleanField(default=False)

    class Meta:
        table = "designers"

class Editor(Model):
    id = fields.IntField(pk=True)
    discord_id = fields.CharField(max_length=50, unique=True)
    discord_username = fields.CharField(max_length=100)
    soft_deleted = fields.BooleanField(default=False)
    
    # a many-to-many relationship needs to only be defined once
    # a single editor can work for multiple creators, and a creator can have multiple editors working for them
    # no need to set nullable = True
    # the way tortoise does it is it creates a join table with no rows, a row being a relation
    creators = fields.ManyToManyField(
        "bot-data.Creator",
        related_name="editors"
    )

    class Meta:
        table = "editors"