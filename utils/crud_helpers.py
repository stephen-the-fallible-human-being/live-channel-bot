import discord
from database.models import Designer

async def add_designer(member: discord.Member):
    # check if already in database
    designer = await Designer.get_or_none(discord_id=str(member.id))

    # if the designer is already in the database, and was not removed
    if designer and not designer.soft_deleted:
        print(f"Designer **{designer.discord_username}** has already been added")
        return
    
    # if the designer is already in the database, but was removed
    if designer and designer.soft_deleted:
        designer.soft_deleted = False
        await designer.save()
        print(f"Reviving Designer **{designer.discord_username}**")
        return
    
    await Designer.create(discord_id=member.id, discord_username=member.name)
    print(f"Designer **{member.discord_username}** has been added")


async def remove_designer(member: discord.Member):
    # get designer
    designer = await Designer.get_or_none(discord_id=str(member.id))

    # assuming that if the designer role is being taken off, they had added been added to the database
    # oh well, gonna add the logic anyways

    # if a corresponding designer entry in the database doesn't exist
    if not designer:
        print(f"Designer **{member.name}** not found in database.")
        return
    
    # if the corresponding designer entry already shows that the designer has been removed
    if designer.soft_deleted:
        print(f"Designer **{member.name}** has already been removed.")
        return
    
    designer.soft_deleted = True
    await designer.save()
    print(f"Designer **{designer.discord_username}** has been removed.")


async def add_editor(member: discord.Member):
    pass


async def remove_editor(member: discord.Member):
    pass