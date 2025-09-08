"""
Database models for the Live Channel Bot
"""
from tortoise import fields, models


class TimestampMixin:
    """Mixin to add created_at and updated_at fields"""
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class GuildConfig(models.Model, TimestampMixin):
    """Server configuration settings"""
    guild_id = fields.BigIntField(unique=True)
    thumbnail_designer_role_id = fields.BigIntField(null=True)
    editor_role_id = fields.BigIntField(null=True)
    overseer_role_id = fields.BigIntField(null=True)
    single_thumbnail_channel = fields.BooleanField(default=False)
    single_thumbnail_channel_id = fields.BigIntField(null=True)
    
    class Meta:
        table = "guild_configs"


class Creator(models.Model, TimestampMixin):
    """YouTube content creators"""
    name = fields.CharField(max_length=100)
    is_active = fields.BooleanField(default=True)
    
    class Meta:
        table = "creators"


class Editor(models.Model, TimestampMixin):
    """Video editors"""
    discord_id = fields.BigIntField(unique=True)
    discord_username = fields.CharField(max_length=100)
    is_active = fields.BooleanField(default=True)
    # Many-to-many relationship with creators
    assigned_creators = fields.ManyToManyField('models.Creator', related_name='assigned_editors')
    
    class Meta:
        table = "editors"


class ThumbnailDesigner(models.Model, TimestampMixin):
    """Thumbnail designers"""
    discord_id = fields.BigIntField(unique=True)
    discord_username = fields.CharField(max_length=100)
    is_active = fields.BooleanField(default=True)
    
    class Meta:
        table = "thumbnail_designers"


class Overseer(models.Model, TimestampMixin):
    """Overseers/managers"""
    discord_id = fields.BigIntField(unique=True)
    discord_username = fields.CharField(max_length=100)
    is_active = fields.BooleanField(default=True)
    
    class Meta:
        table = "overseers"


class ThumbnailCategory(models.Model, TimestampMixin):
    """Thumbnail request category channels"""
    name = fields.CharField(max_length=50, unique=True)
    channel_id = fields.BigIntField(unique=True, null=True)
    is_active = fields.BooleanField(default=True)
    
    class Meta:
        table = "thumbnail_categories"


class Thumbnail(models.Model, TimestampMixin):
    """Completed thumbnail records for export"""
    designer = fields.ForeignKeyField('models.ThumbnailDesigner', related_name='completed_thumbnails')
    creator = fields.ForeignKeyField('models.Creator', related_name='thumbnail_records')
    category = fields.ForeignKeyField('models.ThumbnailCategory', related_name='thumbnail_records')
    youtube_url = fields.CharField(max_length=200)
    
    class Meta:
        table = "thumbnails"