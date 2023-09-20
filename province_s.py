import asyncio #to run the assyncronous processis
import json
import re
from typing import Dict, List

import httpx
from parsel import Selector
from typing_extensions import TypedDict