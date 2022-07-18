from typing import TypedDict, NamedTuple
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium import webdriver


class Car(TypedDict):
    brand: str
    model: str


class CarCard(TypedDict):
    url: str
    image_src: str
    name: str
    milage: str
    color: str
    year: str
    price: str
    site: str


class Session():
    def __init__(self):
        # options = Options()
        # options.add_argument("--headless")
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        print("Driver evoked")

    def close(self):
        self.driver.close()
