from bs4 import BeautifulSoup


def removetooltip(parsed: BeautifulSoup) -> None:
    for span in parsed.find_all("span", {"class": "tooltiptext"}):
        span.replace_with("")


def removecitation(parsed: BeautifulSoup) -> None:
    for sup in parsed.find_all("sup"):
        sup.replace_with("")
