from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from src.parsers.adapter import Car, CarCard
from src.parsers.adapter import Session
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


class AutoRuParser():
    def __init__(self, parameters: Car, session: Session):
        self.driver = session.driver
        self.params = parameters
        self.url = self.compose_url()

    def compose_url(self):
        if self.params.keys() == {'brand', 'model'}:
            url = f"https://auto.ru/cars/{self.params['brand']}/{self.params['model']}/all/"
            return url
        else:
            # TODO: add more parameters
            raise ValueError("No way")

    def parse(self) -> list:
        act = ActionChains(self.driver)
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
            car = CarCard()
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

                # TODO: get image urls from autoru
                # img = item.find_element(By.CLASS_NAME, "Brazzers__image-wrapper")
                # img_link = img.find_element(By.TAG_NAME, "img").get_attribute('src')

            except Exception as e:
                print(f'{e}')
                continue

            if all([name, url, mileage, price, color, year]):
                car['site'] = 'autoru'
                car['name'] = name
                car['url'] = url
                car['image_src'] = 'No'
                car['milage'] = mileage
                car['price'] = price
                car['color'] = color
                car['year'] = year
                result.append(car)

        print("closing")
        self.driver.close()
        return result


if __name__ == "__main__":
    s = Session()
    f = Car(brand="toyota", model="avensis")
    p = AutoRuParser(f, s)
    res = p.parse()
    print(res)
