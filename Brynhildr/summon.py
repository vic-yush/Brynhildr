import discord


async def summonparse(categories: str, source: str, embed: discord.Embed) \
        -> None:
    # Get title
    embed.title = source[source.find("wgTitle") + 10:].split('"', 1)[0]
    await generateicons(categories, embed)
    description = source[source.find("meta name=\"description\" content=") +
                         33:].split('"', 1)[0].replace("&#039;", "'")
    image = source[source.find("og:image\" content=\"") + 19:].split('"', 1)[0]
    embed.description += description
    embed.set_thumbnail(url=image)


async def generateicons(categories: str, embed: discord.Embed) \
        -> None:
    text = ""
    # Assign rarity icons
    if "SSR Summons" in categories:
        text += " <:Rarity_SSR:730441789667934278>"
    elif "SR Summons" in categories:
        text += " <:Rarity_SR:730441789319807009>"
    elif "R Summons" in categories:
        text += " <:Rarity_R:730441789642768464>"
    elif "N Summons" in categories:
        text += " <:Rarity_N:730441824954482728>"
    # Assign element icons
    if "Fire Summons" in categories:
        text += " <:Fire:730845600484032624>"
    elif "Water Summons" in categories:
        text += " <:Water:730845600324780151>"
    elif "Earth Summons" in categories:
        text += " <:Earth:730845600672776202>"
    elif "Wind Summons" in categories:
        text += " <:Wind:730845600479707157>"
    elif "Light Summons" in categories:
        text += " <:Light:730845600915914873>"
    elif "Dark Summons" in categories:
        text += " <:Dark:730845600613924954>"
    embed.description = text + "\n"
