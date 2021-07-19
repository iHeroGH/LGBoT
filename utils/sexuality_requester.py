import requests
from bs4 import BeautifulSoup

BASE_URL = "https://lgbta.wikia.org/wiki/"

class SexualityRequester(object):

    def __init__(self, chosen_sexuality: str):
        self.chosen_sexuality = chosen_sexuality
        self.url = self.get_url()
        self.soup_list = self.get_soup()

    def get_url(self, specific:bool=False):
        """Returns the request URL"""
        return BASE_URL + self.chosen_sexuality.title()

    def get_soup(self):
        """Webscrapes the LGBT Wiki for the sexualities in the letter group"""
        soup = BeautifulSoup(requests.get(self.url).content, "html.parser")
        soup = soup.find("body").find("div", class_="mw-parser-output").find("a")
        self.soup = soup

        return soup

    def get_flag(self):
        """Gets the flag image link for the chosen sexuality"""
        flag_url = self.soup.get("href")
        return flag_url