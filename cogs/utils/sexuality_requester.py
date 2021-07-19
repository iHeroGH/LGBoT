import requests
import PIL
from bs4 import BeautifulSoup

BASE_URL = "https://lgbta.wikia.org/wiki/Category:Sexuality?from="

class SexualityRequester(object):

    def __init__(self, chosen_sexuality: str):
        self.chosen_sexuality = chosen_sexuality
        self.url = self.get_url(self.chosen_sexuality[0])
        self.soups = self.get_soups(self.url)
        self.flg = self.get_flag(self.soups, chosen_sexuality)

    def get_url(self, input_text:str):
        """Returns the request URL"""
        return BASE_URL + input_text[0].upper()

    def get_soups(self, url):
        """Webscrapes the LGBT Wiki for the sexualities in the letter group"""
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        soup = soup.find("body").find("div", class_="category-page__members").find_all("a")
        return soup

    def get_flag(self, soup_list, chosen_sexuality):
        """Gets the flag image link for the chosen sexuality"""
        for soup in soup_list:
            for image in soup.find_all("img"):
                if image["alt"].lower() == chosen_sexuality.lower():
                    return (image['src'])
