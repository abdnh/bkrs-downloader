import functools
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


class Downloader:
    BASE_URL: str
    QUERY_URL: str

    def get_word_soup(self, word: str) -> BeautifulSoup:
        return self._get_word_soup(self.QUERY_URL, self.BASE_URL, word)

    @staticmethod
    @functools.lru_cache
    def _get_word_soup(query_url: str, base_url: str, word: str) -> BeautifulSoup:
        req = requests.get(
            query_url.format(word),
            headers={"User-Agent": "Mozilla/5.0"},
        )
        soup = BeautifulSoup(req.text, "html.parser")
        # absolutify URLs
        for url in soup("a"):
            if url.get("href") is not None:
                url["href"] = urljoin(base_url, url.get("href", ""))
        return soup
