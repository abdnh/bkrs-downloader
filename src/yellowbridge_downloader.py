from typing import List

from .downloader import Downloader


class YellowBridgeDownloader(Downloader):
    BASE_URL = "https://www.yellowbridge.com"
    QUERY_URL = f"{BASE_URL}//chinese/dictionary.php?word={{}}"

    def get_words_with_same_head(self, word: str) -> List[str]:
        soup = self._get_word_soup(word)
        table = soup.select("#sameHead tr")
        return [row.decode() for row in table]

    def get_words_with_same_tail(self, word: str) -> List[str]:
        soup = self._get_word_soup(word)
        table = soup.select("#sameTail tr")
        return [row.decode() for row in table]


if __name__ == "__main__":
    downloader = YellowBridgeDownloader()
    words = ["悠着", "不良少年"]
    for word in words:
        print(downloader.get_words_with_same_head(word))
        print(downloader.get_words_with_same_tail(word))
