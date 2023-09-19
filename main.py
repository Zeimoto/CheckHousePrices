import asyncio #to run the assyncronous processis
import json
import re
from typing import Dict, List

import httpx
from parsel import Selector
from typing_extensions import TypedDict

# await asyncio.wait(0)

#estabelecer headers
BASE_HEADERS = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;",
    "accept-enconding":"gzip, deflate, br",
    "accept-language":"pt-PT,pt;q=0.8"
}
session = httpx.AsyncClient(headers=BASE_HEADERS, follow_redirects=True)

# type hints fo expected results so we can visualize our scraper easier:
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


def parse_property(response: httpx.Response) -> PropertyResult:
    """parse Idealista.com property page"""
    # load response's HTML tree for parsing:
    selector = Selector(text=response.text)
    css = lambda x: selector.css(x).get("").strip()
    css_all = lambda x: selector.css(x).getall()

    data = {}
    # Meta data
    data["url"] = str(response.url)

    # Basic information
    data['title'] = css("h1 .main-info__title-main::text")
    data['location'] = css(".main-info__title-minor::text")
    data['currency'] = css(".info-data-price::text")
    data['price'] = css(".info-data-price span::text")#int(css(".info-data-price span::text").replace(",", ""))
    data['description'] = "\n".join(css_all("div.comment ::text")).strip()
    data["updated"] = selector.xpath(
        "//p[@class='stats-text']"
        "[contains(text(),'updated on')]/text()"
    ).get("").split(" on ")[-1]

    # Features
    data["features"] = {}
    #  first we extract each feature block like "Basic Features" or "Amenities"
    for feature_block in selector.css(".details-property-h3"):
        # then for each block we extract all bullet points underneath them
        label = feature_block.xpath("text()").get()
        features = feature_block.xpath("following-sibling::div[1]//li")
        data["features"][label] = [
            ''.join(feat.xpath(".//text()").getall()).strip()
            for feat in features
        ]

    # Images
    # the images are tucked away in a javascript variable.
    # We can use regular expressions to find the variable and parse it as a dictionary:
    image_data = re.findall(
        "fullScreenGalleryPics\s*:\s*(\[.+?\]),", 
        response.text
    )[0]
    # print("Isto é o response.text:",image_data)
    # we also need to replace unquoted keys to quoted keys (i.e. title -> "title"):
    images = json.loads(re.sub(r'(\w+?):([^/])', r'"\1":\2', image_data))
    # print(images)
    data['images'] = dict()
    data['plans'] = []
    for image in images:
        # print(image)
        site_url = str(response.url).split("/imovel")[0]
        url = (site_url + image['imageUrl'])
        # print(response.url)
        if image['isPlan']:
            data['plans'].append(url)
        else:
            data['images'][image['tag']] = url
    return data


async def scrape_properties(urls: List[str]) -> List[PropertyResult]:
    """Scrape Idealista.com properties"""
    properties = []
    to_scrape = [session.get(url) for url in urls]
    # tip: asyncio.as_completed allows concurrent scraping - super fast!
    for response in asyncio.as_completed(to_scrape):
        response = await response
        if response.status_code != 200:
            print(f"can't scrape property: {response.url}")
            continue
        properties.append(parse_property(response))
    return properties

async def run():
    urls = ["https://www.idealista.pt/imovel/32508835/","https://www.idealista.pt/imovel/32750926/"]
    data = await scrape_properties(urls)
    print(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(run())