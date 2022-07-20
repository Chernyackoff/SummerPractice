from src.parsers.autoru_parser import AutoRuParser
from src.parsers.avito_parser import AvitoParser
from src.parsers.service_parts import *


class MainParser():
    def __init__(self, params: Car):
        self.autoru = AutoRuParser(params)
        self.avito = AvitoParser(params)

    def parse(self) -> list[CarCard]:
        res: list[CarCard] = []
        try:
            res.extend(self.avito.parse())

            res.extend(self.autoru.parse())
        except ValueError as e:
            return None
        return res
