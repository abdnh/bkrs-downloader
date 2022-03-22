from typing import List

from .downloader import Downloader


class YellowBridgeDownloader(Downloader):
    BASE_URL = "https://www.yellowbridge.com"
    QUERY_URL = f"{BASE_URL}//chinese/dictionary.php?word={{}}"

    # def get_words_with_same_head(self, word: str) -> List[str]:
    #     soup = self._get_word_soup(word)
    #     table = soup.select("#sameHead tr")
    #     return [row.decode() for row in table]

    # def get_words_with_same_tail(self, word: str) -> List[str]:
    #     soup = self._get_word_soup(word)
    #     table = soup.select("#sameTail tr")
    #     return [row.decode() for row in table]

    def _apply_table_styles(self, table):
        table[
            "style"
        ] = "border-style: none; border-collapse: collapse; background: white; padding: 0; border-spacing: 1px; border-width: 1px;"
        caption = table.select_one("caption")
        if caption:
            caption[
                "style"
            ] = "  font-size: 1.0; font-weight: bold; padding: 4px 5px 3px 5px; color: #009; background: #fc0; border-style: none; border-radius: 5px 5px 0 0;"
        trs = table.find_all("tr")
        for i in range(1, len(trs), 2):
            trs[i]["style"] = "background: #f8f9f7;"

    def get_words_with_same_head(self, word: str) -> str:
        soup = self._get_word_soup(word)
        table = soup.find(id="sameHead")
        if not table:
            return ""
        self._apply_table_styles(table)
        table["style"] += "float: left; width: 380px; margin: 5px 0 0 5px;"
        return table.decode()

    def get_words_with_same_tail(self, word: str) -> str:
        soup = self._get_word_soup(word)
        table = soup.find(id="sameTail")
        if not table:
            return ""
        self._apply_table_styles(table)
        table["style"] += "float: right; width: 380px; margin: 5px 5px 0 0;"
        return table.decode()


if __name__ == "__main__":
    downloader = YellowBridgeDownloader()
    words = ["悠着", "不良少年"]
    for word in words:
        print(downloader.get_words_with_same_head(word))
        print(downloader.get_words_with_same_tail(word))
