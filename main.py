import asyncio
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from pathlib import PurePath

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
            found_text.append(text_container.text)
    return found_text


async def sanitize_result(parser, URL: str):
    result = await parser(URL)
    return set(result)


if __name__ == "__main__":
    with asyncio.Runner() as runner:
        sanitized = runner.run(sanitize_result(parse_html, URL=URL))
    print(len(sanitized))
    print(sanitized)
