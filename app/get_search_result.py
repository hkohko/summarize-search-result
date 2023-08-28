import asyncio
from app.locations import Directories
from bs4 import BeautifulSoup
from aiohttp import ClientSession

APP_DIR = Directories.APP_DIR
MAIN_DIR = Directories.MAIN_DIR
SAMPLE_TEXT = Directories.SAMPLE_TEXT
URL = r"https://html.duckduckgo.com/html/?q=i+want+to+eat+your+pancreas"


async def make_request(URL: str):
    async with ClientSession() as session:
        async with session.get(URL) as resp:
            result = await resp.text()
    return result


async def parse_html(URL: str):
    page_text = await make_request(URL)
    soup = BeautifulSoup(page_text, "lxml")
    body = soup.find("body", {"class": "body--html"})
    main_div = body.find("div", {"class": "serp__results"})
    inner_div = main_div.find("div", {"id": "links", "class": "results"})
    search_result = inner_div.find_all("div", {"class": True})
    found_text = []
    for result in search_result:
        text_container = result.find("a", {"class": "result__snippet"})
        if text_container is not None:
            text: str = text_container.text
            found_text.append(text.encode("utf-8"))
    return found_text


async def sanitize_result(parser, URL: str) -> set[str]:
    result = await parser(URL)
    remove_dupe = set(result)
    return remove_dupe


async def main(URL: str):
    sanitized = await sanitize_result(parse_html, URL=URL)
    result = [desc.decode("utf-8") for desc in sanitized]
    return " ".join(result)


if __name__ == "__main__":
    to_write = asyncio.run(main(URL))
    with open(SAMPLE_TEXT.joinpath("text_1.txt"), "w", encoding="utf-8") as file:
        file.write(to_write)
