from typing import List, Optional
import requests
import functools
import bs4
from bs4 import BeautifulSoup


class BkrsDownloader:
    QUERY_URL = "https://bkrs.info/slovo.php?ch={}"

    def __init__(self):
        pass

    @functools.lru_cache
    def _get_word_soup(self, word: str) -> BeautifulSoup:
        req = requests.get(
            self.QUERY_URL.format(word), headers={"User-Agent": "Mozilla/5.0"}
        )
        soup = BeautifulSoup(req.text, "html.parser")
        return soup

    def get_definitions(self, word: str) -> List[str]:
        soup = self._get_word_soup(word)
        ru_el = soup.select_one(".ru")
        defs = []
        if ru_el:
            # word
            divs = soup.select(".ru > div")
            if len(divs) == 0:
                # single definition
                defs.append(ru_el.decode())
            else:
                for e in divs:
                    # the definition section sometimes contains examples; skip them
                    if e.select_one(".ex"):
                        continue

                    text = e.get_text().strip()
                    defs.append(text)
        else:
            # phrase?
            table = soup.select_one(".tbl_bywords")
            if table:
                defs.append(table.decode())

        return defs

    def get_examples(self, word: str, highlight_color: Optional[str] = None) -> List:
        soup = self._get_word_soup(word)
        # FIXME: this doesn't seem to return example elements in DOM order?!
        divs = soup.select("#examples > div")
        examples = []
        for example_div in divs:
            highlighted_el = example_div.select_one("span")
            if highlighted_el:
                if highlight_color:
                    highlighted_el["class"] = []
                    color = highlight_color
                else:
                    color = (
                        highlighted_el["class"][0] if highlighted_el["class"] else ""
                    )
                if color:
                    highlighted_el["style"] = f"color: {color};"
            examples.append(example_div.decode())
        return examples


if __name__ == "__main__":
    downloader = BkrsDownloader()
    words = ["没的说", "不巧的", "不良少年", "少年"]
    for word in words:
        # print(downloader.get_definitions(word))
        for definition in downloader.get_definitions(word):
            print(definition)
        for example in downloader.get_examples(word):
            print(example)
