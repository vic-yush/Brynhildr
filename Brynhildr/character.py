import discord


async def characterparse(categories: str, source: str, embed: discord.Embed) \
        -> None:
    # Get title
    embed.title = source[source.find("wgTitle") + 10:].split('"', 1)[0]
    await generateicons(categories, embed)
    description = source[source.find("meta name=\"description\" content=") +
                         33:].split('"', 1)[0].replace("&#039;", "'")
    obtain = generateobtain(source)
    image = source[source.find("og:image\" content=\"") + 19:].split('"', 1)[0]
    embed.description += description
    embed.set_thumbnail(url=image)
    embed.add_field(name="How to Recruit", value=obtain)


async def generateicons(categories: str, embed: discord.Embed) \
        -> None:
    text = ""
    # Assign rarity icons
    if "SSR Characters" in categories:
        text += " <:Rarity_SSR:730441789667934278>"
    elif "SR Characters" in categories:
        text += " <:Rarity_SR:730441789319807009>"
    elif "R Characters" in categories:
        text += " <:Rarity_R:730441789642768464>"
    # Assign element icons
    if "Fire Characters" in categories:
        text += " <:Fire:730845600484032624>"
    elif "Water Characters" in categories:
        text += " <:Water:730845600324780151>"
    elif "Earth Characters" in categories:
        text += " <:Earth:730845600672776202>"
    elif "Wind Characters" in categories:
        text += " <:Wind:730845600479707157>"
    elif "Light Characters" in categories:
        text += " <:Light:730845600915914873>"
    elif "Dark Characters" in categories:
        text += " <:Dark:730845600613924954>"
    # Assign race icons
    # Check each race, as multirace options exist
    if "Draph Characters" in categories:
        text += " <:Draph1:731182416441376808><:Draph2:731182416475193464>" \
                  "<:Draph3:731182416407822376><:Draph4:731182416030466070>"
    if "Erune Characters" in categories:
        text += " <:Erune1:731181941662941184><:Erune2:731181942170583060>" \
                  "<:Erune3:731181941474197505><:Erune4:731181941646426133>"
    if "Harvin Characters" in categories:
        text += " <:Harvin1:731177969992859844>" \
                  "<:Harvin2:731177970177278023><:Harvin3:731177970416353280>" \
                  "<:Harvin4:731177970353569854>"
    if "Human Characters" in categories:
        text += " <:Human1:731174811774091304><:Human2:731174811518238822>" \
                  "<:Human3:731174811648262155><:Human4:731174811857977384>"
    if "Other Characters" in categories:
        text += " <:Unknown1:731183072850083942>" \
                  "<:Unknown2:731183073026375811>" \
                  "<:Unknown3:731183073101742110>" \
                  "<:Unknown4:731183072862666813>"
    if "Primal Characters" in categories:
        text += " <:Primal1:731173612035244052>" \
                  "<:Primal2:731173611918065684><:Primal3:731173290848157696>" \
                  "<:Primal4:731173290806214736>"
    # Assign weapon proficiency icons
    # Check each type, as some characters have multiple proficiencies
    if "Sabre Characters" in categories:
        text += " <:Sabre1:730454365248159855><:Sabre2:730454663941324861>"
    if "Dagger Characters" in categories:
        text += " <:Dagger1:730455370233020558><:Dagger2:730455370673291314>"
    if "Spear Characters" in categories:
        text += " <:Spear1:730456104898920458><:Spear2:730456104840200363>"
    if "Axe Characters" in categories:
        text += " <:Axe1:730456397942095943><:Axe2:730456397556482110>"
    if "Staff Characters" in categories:
        text += " <:Staff1:730456836221829173><:Staff2:730456836310040677>"
    if "Gun Characters" in categories:
        text += " <:Gun1:730457164552077382><:Gun2:730457164266864784>"
    if "Melee Characters" in categories:
        text += " <:Melee1:730457549672939621><:Melee2:730457549337264139>"
    if "Bow Characters" in categories:
        text += " <:Bow1:730457814627254322><:Bow2:730457814551756840>"
    if "Harp Characters" in categories:
        text += " <:Harp1:730458095591096420><:Harp2:730458095221997580>"
    if "Katana Characters" in categories:
        text += " <:Katana1:730458503742750822><:Katana2:730458504011317319>"
    embed.description = text + "\n"


def generateobtain(source: str) -> str:
    raw = source[source.find("How to Recruit") + 14:].split("</tbody>", 1)[0]
    link = raw[raw.find("<a href=\"") + 9:].split('"', 1)[0]
    text = raw[raw.find("title=\"") + 7:].split('"', 1)[0]
    return "[" + text + "](https://gbf.wiki" + link + ")"
