from urllib.parse import urljoin
import functools
import requests
from bs4 import BeautifulSoup


class Downloader:
    BASE_URL: str
    QUERY_URL: str

    @functools.lru_cache
    def _get_word_soup(self, word: str) -> BeautifulSoup:
        req = requests.get(
            self.QUERY_URL.format(word),
            headers={"User-Agent": "Mozilla/5.0"},
        )
        soup = BeautifulSoup(req.text, "html.parser")
        # absolutify URLs
        for url in soup("a"):
            if url.get("href") is not None:
                url["href"] = urljoin(self.BASE_URL, url.get("href", ""))
        return soup
