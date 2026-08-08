import json
import random
import re
import requests
import sys
import time
from typing import Iterable, Callable, TypeVar
from datetime import datetime

from py_common.util import guess_nationality, scraper_args
import py_common.log as log
from py_common.deps import ensure_requirements

ensure_requirements("cloudscraper", "lxml")

import cloudscraper  # noqa: E402
from lxml import html  # noqa: E402


def scrape(url: str, retries=0):
    try:
        scraped = scraper.get(url, timeout=(3, 7))
    except requests.exceptions.Timeout as exc_time:
        log.debug(f"Timeout: {exc_time}")
        return scrape(url, retries + 1)
    except Exception as e:
        log.error(f"scrape error {e}")
        sys.exit(1)
    if scraped.status_code >= 400:
        if retries < 10:
            wait_time = random.randint(1, 4)
            log.debug(f"HTTP Error: {scraped.status_code}, waiting {wait_time} seconds")
            time.sleep(wait_time)
            return scrape(url, retries + 1)
        log.error(f"HTTP Error: {scraped.status_code}, giving up")
        sys.exit(1)

    return html.fromstring(scraped.content)