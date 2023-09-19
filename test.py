import asyncio 
import httpx
from datetime import datetime
from typing import Dict, List
from typing_extensions import TypedDict
import json

BASE_HEADERS = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;",
    "accept-enconding":"gzip, deflate, br",
    "accept-language":"pt-PT,pt;q=0.8"
}
session = httpx.AsyncClient(headers=BASE_HEADERS, follow_redirects=True)

class PropertyResult(TypedDict):
    url: str
    title: str
    location: str
    price: int
    currency: str
    description: str
    updated: str
    features: Dict[str, List[str]]
    images: Dict[str, List[str]]
    plans: List[str]

async def main():
    urls = ["https://www.idealista.pt/","https://www.google.com/"]
    data = await second_coroutine(urls)
    print(data)
    # for response in asyncio.as_completed(session.get(url) for url in urls):
        # await response
        # print(response.statuscode)



async def second_coroutine(urls: List[str]):
    responses = dict()
    to_scrape = [session.get(url) for url in urls]
    for response in asyncio.as_completed(to_scrape):
        response = await response
        responses[response.url] = response.content
    return responses


asyncio.run(main=main())