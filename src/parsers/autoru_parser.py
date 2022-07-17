from adapter import Car


class AutoRuParser():
    def __init__(self, parameters: Car):
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
        pass
