import requests
import aiohttp
import bs4
import utils as localutils

BASE_URL = "https://lgbta.wikia.org/wiki/"

class Requester(object):
    """
    Requester handles all the data transfers between Discord and the LGBTA wiki
    """

    cache = {}

    def __init__(self, chosen_topic: str, soup = None):
        self.chosen_topic = chosen_topic
        self.soup = soup
        self.cache[self.chosen_topic] = self

    @property
    def soup(self):
        return self._soup

    @soup.setter 
    def soup(self, value):
        if value:
            self.check_exists(value)
            self._soup = self.refine_soup(value)

    def __repr__(self):
        """The string representation of the Requester class"""

        return f"Requester(chosen_topic={self.chosen_topic})"

    @property
    def url(self) -> str: 
        """Returns the request URL"""

        return BASE_URL + self.chosen_topic.title()
        
    def check_exists(self, soup) -> bool:
        """Checks if the Wiki page exists"""

        content_to_check = soup.find("body").find("div", class_="mw-parser-output")
        if not content_to_check:
            # print(self.chosen_topic)
            raise localutils.TopicNotFoundError(self.chosen_topic)

    @classmethod
    async def get_requester(cls, chosen_topic: str):
        """Webscrapes the LGBT Wiki for the chosen topic"""

        if chosen_topic in cls.cache:
            return cls.cache[chosen_topic]

        requester = cls(chosen_topic)
        async with aiohttp.ClientSession() as session:
            async with session.get(requester.url) as response:
                soup = bs4.BeautifulSoup(await response.text(), "html.parser")
        requester.soup = soup
        
        return requester

    def refine_soup(self, soup) -> bs4.element.Tag:
        """Refines the soup to get the important content of the page"""

        return soup.find("body").find("div", class_="mw-parser-output")

    def get_info(self) -> str:
        """Gets the topic's info"""

        all_p = self.soup.find_all("p")
        # Remove every element from the list that has a caption class and that is smaller than 130 characters
        all_p = [x for x in all_p if "class" not in x.attrs and len(x.text) > 130]
        info = all_p[0].text
        return info

    def get_flag(self) -> str:
        """Gets the flag image link for the chosen sexuality"""

        flag_url = self.soup.find("figure").find("a").get("href")
        return flag_url
