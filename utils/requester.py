import requests
from bs4 import BeautifulSoup

BASE_URL = "https://lgbta.wikia.org/wiki/"

class Requester(object):

    def __init__(self, chosen_topic: str):
        self.chosen_topic = chosen_topic
        self.url = self.get_url()
        self.soup = self.get_soup()

    def get_url(self, specific:bool=False):
        """Returns the request URL"""
        return BASE_URL + self.chosen_topic.title()

    def get_soup(self):
        """Webscrapes the LGBT Wiki for the chosen topic"""
        soup = BeautifulSoup(requests.get(self.url).content, "html.parser")
        soup = soup.find("body").find("div", class_="mw-parser-output")

        return soup

    def get_info(self):
        """Gets the topic's info"""
        all_p = self.soup.find_all("p")
        # Pop every element from the list that has a caption class
        all_p = [x for x in all_p if "class" not in x.attrs and len(x.text) > 130]
        info = all_p[0].text
        return info

    def get_flag(self):
        """Gets the flag image link for the chosen sexuality"""
        flag_url = self.soup.find("figure").find("a").get("href")
        return flag_url