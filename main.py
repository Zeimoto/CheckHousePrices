import asyncio #to run the assyncronous processis
import json
import re
from typing import Dict, List

import httpx
from parsel import Selector
from typing_extensions import TypedDict
import numpy

#estabelecer headers
BASE_HEADERS = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;",
    "accept-enconding":"gzip, deflate, br",
    "accept-language":"pt-PT,pt;q=0.8"
}
session = httpx.AsyncClient(headers=BASE_HEADERS, follow_redirects=True)

