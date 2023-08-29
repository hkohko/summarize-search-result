import asyncio
from os import listdir
from app.locations import Directories
from bs4 import BeautifulSoup
from aiohttp import ClientSession

APP_DIR = Directories.APP_DIR
MAIN_DIR = Directories.MAIN_DIR
SAMPLE_TEXT = Directories.SAMPLE_TEXT

BASE_URL = r"https://html.duckduckgo.com/html/?q="
URL = r"https://html.duckduckgo.com/html/?q=i+want+to+eat+your+pancreas"
URL_2 = r"https://html.duckduckgo.com/html/?q=watashi+ni+tenshi+ga+maiorita"
URL_3 = r"https://html.duckduckgo.com/html/?q=who+is+donald+trump"


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
    sanitized = await parse_html(URL=URL)
    result = [desc.decode("utf-8") for desc in sanitized]
    return " ".join(result)


def user_input():
    entry = input("Search for: ")
    query_text = entry.replace(" ", "+")
    return query_text


if __name__ == "__main__":
    while True:
        query = user_input()
        to_write = asyncio.run(main(BASE_URL + query))
        nums = [idx for idx, _ in enumerate(listdir(Directories.SAMPLE_TEXT))]
        numbering = 0 if len(nums) == 0 else len(nums) + 1
        with open(SAMPLE_TEXT.joinpath(f"text_{numbering}.txt"), "w", encoding="utf-8") as file:
            file.write(to_write)
