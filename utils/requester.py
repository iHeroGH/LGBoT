import requests
import bs4
import utils as localutils

BASE_URL = "https://lgbta.wikia.org/wiki/"

class Requester(object):
    """
    Requester handles all the data transfers between Discord and the LGBTA wiki
    """

    def __init__(self, chosen_topic: str):
        self.chosen_topic = chosen_topic
        self.url = self.get_url()
        self.soup = self.get_soup()
        self.check_exists()
        self.soup = self.refine_soup()

    def __repr__(self):
        """The string representation of the Requester class"""
        return f"Requester(chosen_topic={self.chosen_topic})"

    def get_url(self, specific:bool=False) -> str: 
        """Returns the request URL"""
        return BASE_URL + self.chosen_topic.title()
        
    def check_exists(self) -> bool:
        """Checks if the wiki page exists"""
        content_to_check = self.soup.find("body").find("div", class_="mw-parser-output")
        if not content_to_check:
            print(self.chosen_topic)
            raise localutils.TopicNotFoundError(self.chosen_topic)

    def get_soup(self) -> bs4.BeautifulSoup:
        """Webscrapes the LGBT Wiki for the chosen topic"""
        return bs4.BeautifulSoup(requests.get(self.url).content, "html.parser")

    def refine_soup(self) -> bs4.element.Tag:
        """Refines the soup to get the important content of the page"""
        return self.soup.find("body").find("div", class_="mw-parser-output")

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