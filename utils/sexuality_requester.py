import requests
from bs4 import BeautifulSoup

BASE_URL = "https://lgbta.wikia.org/wiki/Category:Sexuality?from="

class SexualityRequester(object):

    def __init__(self, chosen_sexuality: str):
        self.chosen_sexuality = chosen_sexuality
        self.url = self.get_url()
        self.soup_list = self.get_soups()

    def get_url(self):
        """Returns the request URL"""
        return BASE_URL + self.chosen_sexuality[0].upper()

    def get_soups(self):
        """Webscrapes the LGBT Wiki for the sexualities in the letter group"""
        soup = BeautifulSoup(requests.get(self.url).content, "html.parser")
        soup_list = soup.find("body").find("div", class_="category-page__members").find_all("a")
        self.soup_list = soup_list

        return soup_list

    def get_flag(self):
        """Gets the flag image link for the chosen sexuality"""
        for soup in self.soup_list:
            for image in soup.find_all("img"):
                if image["alt"].lower() == self.chosen_sexuality.lower():
                    return (image['src'])
