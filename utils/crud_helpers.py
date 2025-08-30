import discord
from database.models import Designer, Editor

async def add_designer(member: discord.Member):
    # check if already in database
    designer = await Designer.get_or_none(discord_id=str(member.id))

    # if the designer is already in the database, and was not removed
    if designer and not designer.soft_deleted:
        print(f"**{member.name}** has already been added as a **Designer**.")
        return
    
    # if the designer is already in the database, but was removed
    if designer and designer.soft_deleted:
        designer.soft_deleted = False
        await designer.save()
        print(f"**{member.name}** has been revived as a **Designer**.")
        return
    
    await Designer.create(discord_id=str(member.id), discord_username=member.name)
    print(f"**{member.name}** has been added as a **Designer**")


async def remove_designer(member: discord.Member):
    # get designer
    designer = await Designer.get_or_none(discord_id=str(member.id))

    # assuming that if the designer role is being taken off, then the designer role was given before
    # meaning, they had to have been added to the db, if not, oh well, they were never added, they're being taken off anyways
    # gonna add the logic anyways

    # if a corresponding designer entry in the database doesn't exist
    if not designer:
        print(f"**{member.name}** was not previously added as a **Designer**.")
        return
    
    # if the corresponding designer entry already shows that the designer has been removed
    if designer.soft_deleted:
        print(f"**{member.name}** has already been removed as a **Designer**.")
        return
    
    designer.soft_deleted = True
    await designer.save()
    print(f"**{member.name}** has been removed as a **Designer**.")


async def add_editor(member: discord.Member):
    # check if already added
    editor= await Editor.get_or_none(discord_id=str(member.id))

    # if already added, and not previously removed
    if editor and not editor.soft_deleted:
        print(f"**{member.name}** has already been added as an **Editor**")
        return

    # if already added, but previously removed
    if editor and editor.soft_deleted:
        editor.soft_deleted = False
        await editor.save()
        print(f"**{member.name}** has been revived as an **Editor**")
        return

    await Editor.create(discord_id=str(member.id), discord_username=member.name)
    print(f"**{member.name}** has been added as an **Editor**")


async def remove_editor(member: discord.Member):
    # get editor
    editor = await Editor.get_or_none(discord_id=str(member.id)) 

    # if editor couldn't be found
    if not editor:
        print(f"**{member.name}** was not previously added as an **Editor**.")
        return
    
    # if editor was found, but was already removed
    if editor.soft_deleted:
        print(f"**{member.name}** has already been removed as an **Editor**.")
        return

    editor.soft_deleted = True
    await editor.save()
    print(f"**{member.name}** has been removed as an **Editor**.")