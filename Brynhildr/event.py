<<<<<<< HEAD
import discord
from util import *


async def eventparse(categories: list, source: str, embed: discord.Embed,
                     simple: bool) -> None:
    parsed = BeautifulSoup(source, 'html.parser')
    # Generate the title of the embed
    embed.title = source[source.find("wgTitle") + 10:].split('"', 1)[0]
    if parsed.find("blockquote"):
        description = parsed.find("blockquote").text
    else:
        description = ""
    if "Unite and Fight" in categories:
        raw = source[source.find("features"):].split("<\p>", 1)[0]
        element = BeautifulSoup(raw, "html.parser").find("span").text
        description += "This iteration of Unite and Fight features **" + \
                       element + "** enemies."
    image = parsed.find("img")["src"]
    embed.description = description
    embed.set_thumbnail(url="https://gbf.wiki/" + image)
    if not simple:
        if "Unite and Fight" in parsed.find("title").text:
            embed.add_field(name="It's complicated", value="You're better off "
                                                           "just reading the "
                                                           "full article.")
        else:
            rewards = await generaterewards(source)
            embed.add_field(name="Notable Rewards", value=rewards)


async def generaterewards(source: str) -> str:
    output = ""
    # Trim
    raw = source[source.find("id=\"Notable_Rewards"):].split("</div>", 1)[0]
    parsed = BeautifulSoup(raw, "html.parser")
    div = parsed.find("div")
    # Get the links
    for a in div.find_all("a"):
        # Links are composed of an image component and a text component... both
        # wrapped in the same link for some reason. This checks for and discards
        # The image component.
        if a.find_all("img"):
            continue
        output += "[" + a.text + "](https://gbf.wiki" + a["href"] + ")\n"
    return output
