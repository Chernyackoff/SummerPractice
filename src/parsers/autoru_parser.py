from src.parsers.service_parts import Car, CarCard
from src.parsers.service_parts import Session
from selenium.webdriver.common.by import By


class AutoRuParser:
    def __init__(self, parameters: Car):
        self.driver = Session().driver
        self.params = parameters
        self.url = self.compose_url()

    def compose_url(self):
        if self.params.keys() == {'brand', 'model'}:
            url = f"https://auto.ru/cars/{self.params['brand']}/{self.params['model']}/all/"
            return url
        else:
            # TODO: add more parameters
            raise ValueError("No way")

    def get_img(self, item) -> str:
        try:
            img = item.find_elements(By.CLASS_NAME, 'Brazzers__page')
            img_url = img[1].find_element(By.TAG_NAME, 'img').get_attribute('src')
            return img_url
        except Exception:
            return 'No'

    def parse(self) -> list[CarCard]:
        self.driver.get(self.url)
        result = []

        # get all car cards
        try:
            cars = self.driver.find_elements(By.CLASS_NAME, "ListingItem")
        except Exception as e:
            print(f"Error: {e}")
            raise ValueError("No items found")

        # parse car info
        for item in cars:
            try:
                info = item.find_element(By.CLASS_NAME, "ListingItemTitle__link")
                name = info.text
                url = info.get_attribute('href')

                info = item.find_elements(By.CLASS_NAME, "ListingItemTechSummaryDesktop__column")
                color = info[-1].find_elements(By.CLASS_NAME, "ListingItemTechSummaryDesktop__cell")[-1].text

                price = item.find_element(By.CLASS_NAME, "ListingItemPrice__content").text
                price = ''.join(price.split("&nbsp;"))

                mileage = item.find_element(By.CLASS_NAME, "ListingItem__kmAge").text
                mileage = ''.join(mileage.split("&nbsp;"))

                year = item.find_element(By.CLASS_NAME, "ListingItem__year").text

                img_url = self.get_img(item)

            except Exception as e:
                print(f'{e}')
                continue

            if all([name, url, mileage, price, color, year]):
                car = CarCard(site='autoru',
                              name=name,
                              mileage=mileage,
                              url=url,
                              image_src=img_url,
                              price=price,
                              color=color,
                              year=year
                              )

                result.append(car)

        self.driver.close()
        return result
