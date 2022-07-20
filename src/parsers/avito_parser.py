from src.parsers.service_parts import Car, CarCard
from src.parsers.service_parts import Session
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class AvitoParser:
    def __init__(self, parameters: Car):
        self.driver = Session().driver
        self.params = parameters
        self.url = self.compose_url()

    def compose_url(self) -> str:
        if self.params.keys() == {'brand', 'model'}:
            url = f'https://www.avito.ru/rossiya/avtomobili/{self.params["brand"]}/{self.params["model"]}'
            return url
        else:
            # TODO: add more parameters
            raise ValueError('No way')

    def parse_car(self, item) -> CarCard:
        while True:
            try:
                item.click()
                break
            except Exception:
                print('unclickable')
        self.driver.switch_to.window(window_name=self.driver.window_handles[-1])

        try:
            name, year = WebDriverWait(self.driver, 2).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'title-info-title-text'))).text.split(', ')
            url = self.driver.current_url
            price = WebDriverWait(self.driver, 2).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'js-item-price')))
            price = self.driver.find_element(By.CLASS_NAME, 'js-item-price')
            price = price.get_attribute('content')

            info = self.driver.find_element(By.CLASS_NAME, 'params-paramsList-2PiKQ')
            info = info.find_elements(By.TAG_NAME, 'li')

            mileage = info[2].text

            color = info[-3].text

            image_link = self.driver.find_element(By.TAG_NAME, 'img').get_attribute('src')

        except Exception as e:
            print(f'{e}')
            raise ValueError

        list_of_keys = [name, year, mileage, url, price, color]
        if all(list_of_keys) and url != 'about:blank':
            car = CarCard(site='avito',
                          name=name,
                          mileage=mileage,
                          url=url,
                          image_src=image_link,
                          price=price,
                          color=color,
                          year=year
                          )
        else:
            raise ValueError("Parsing error, wrong info parsed")

        self.driver.close()
        self.driver.switch_to.window(window_name=self.driver.window_handles[0])
        print(car)
        return car

    def parse(self) -> list[CarCard]:
        self.driver.set_page_load_timeout(30)
        try:
            self.driver.get(self.url)
        except Exception:
            pass

        try:
            cars = self.driver.find_elements(By.CLASS_NAME, "js-catalog-item-enum")
        except Exception as e:
            print("Nothing")
            raise ValueError("Nothing found")

        car_cards = []
        for count, item in enumerate(cars):
            if count > 15:
                break
            try:
                card = self.parse_car(item)
            except ValueError:
                self.driver.close()
                self.driver.switch_to.window(window_name=self.driver.window_handles[0])
                continue

            car_cards.append(card)

        self.driver.close()
        return car_cards


if __name__ == "__main__":
    s = Session()
    f = Car(brand="toyota", model="avensis")
    p = AvitoParser(f, s)
    res = p.parse()
