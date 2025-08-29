from tortoise import fields
from tortoise.models import Model

class GuildConfig(Model):
    id = fields.IntField(pk=True)
    guild_id = fields.CharField(max_length=50)
    thumbnail_designer_role_id = fields.CharField(max_length=50, null=True)
    editor_role_id = fields.CharField(max_length=50, null=True)

class Designer(Model):
    id = fields.IntField(pk=True)
    discord_id = fields.CharField(max_length=50, unique=True)
    discord_username = fields.CharField(max_length=100)
    soft_deleted = fields.BooleanField(default=False)

    class Meta:
        table = "designers"

class Creator(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    soft_deleted = fields.BooleanField(default=False)

    class Meta:
        table = "creators"