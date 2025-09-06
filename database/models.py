"""
Database models for the Live Channel Bot
"""
from tortoise import fields, models
from datetime import datetime


class TimestampMixin:
    """Mixin to add created_at and updated_at fields"""
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class GuildConfig(models.Model, TimestampMixin):
    """Server configuration settings"""
    guild_id = fields.BigIntField(unique=True, description="Discord server ID")
    thumbnail_designer_role_id = fields.BigIntField(null=True, description="Role ID for thumbnail designers")
    editor_role_id = fields.BigIntField(null=True, description="Role ID for editors")
    overseer_role_id = fields.BigIntField(null=True, description="Role ID for overseers")
    single_thumbnail_channel = fields.BooleanField(default=False, description="Whether to use a single channel for all thumbnail requests")
    single_thumbnail_channel_id = fields.BigIntField(null=True, description="Discord channel ID for single thumbnail requests")
    
    class Meta:
        table = "guild_configs"


class Creator(models.Model, TimestampMixin):
    """YouTube content creators"""
    name = fields.CharField(max_length=100, description="Display name")
    is_active = fields.BooleanField(default=True, description="Whether the creator is active")
    
    class Meta:
        table = "creators"


class Editor(models.Model, TimestampMixin):
    """Video editors"""
    discord_id = fields.BigIntField(unique=True, description="Discord user ID")
    discord_username = fields.CharField(max_length=100, description="Discord username")
    is_active = fields.BooleanField(default=True, description="Whether the editor is active")
    # Many-to-many relationship with creators
    assigned_creators = fields.ManyToManyField('models.Creator', related_name='assigned_editors', description="Creators this editor is assigned to")
    
    class Meta:
        table = "editors"


class Designer(models.Model, TimestampMixin):
    """Thumbnail designers"""
    discord_id = fields.BigIntField(unique=True, description="Discord user ID")
    discord_username = fields.CharField(max_length=100, description="Discord username")
    is_active = fields.BooleanField(default=True, description="Whether the designer is active")
    
    class Meta:
        table = "designers"


class Overseer(models.Model, TimestampMixin):
    """Overseers/managers"""
    discord_id = fields.BigIntField(unique=True, description="Discord user ID")
    discord_username = fields.CharField(max_length=100, description="Discord username")
    is_active = fields.BooleanField(default=True, description="Whether the overseer is active")
    
    class Meta:
        table = "overseers"


class ThumbnailCategory(models.Model, TimestampMixin):
    """Thumbnail request category channels"""
    category_name = fields.CharField(max_length=50, unique=True, description="Category name (e.g., Gaming, Tech)")
    channel_id = fields.BigIntField(unique=True, description="Discord channel ID")
    channel_name = fields.CharField(max_length=100, description="Discord channel name")
    is_active = fields.BooleanField(default=True, description="Whether the category is active")
    
    class Meta:
        table = "thumbnail_categories"


class Thumbnail(models.Model, TimestampMixin):
    """Completed thumbnail records for export"""
    designer = fields.ForeignKeyField('models.Designer', related_name='completed_thumbnails', description="Designer who completed it")
    creator = fields.ForeignKeyField('models.Creator', related_name='thumbnail_records', description="Creator the video was for")
    youtube_url = fields.CharField(max_length=200, description="YouTube video URL")
    category = fields.CharField(max_length=50, description="Video category")
    completed_at = fields.DatetimeField(auto_now_add=True, description="When the thumbnail was completed")
    
    class Meta:
        table = "thumbnails"