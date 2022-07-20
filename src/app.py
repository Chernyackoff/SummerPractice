from flask import Flask, render_template, url_for
from src.parsers.adapter import MainParser
from src.parsers.service_parts import Car, CarCard

app = Flask(__name__)

models = {
    'toyota': ['corolla', 'chaser', 'gt86', 'supra'],
    'subaru': ['impreza'],
    'honda': ['s2000', 'civic'],
    'mazda': ['rx-7']
}
brands = models.keys()


@app.route('/')
def index():
    return render_template('main.html', source=url_for('static', filename='ico.jpg'), brands=brands,
                           models=models)


@app.route('/<brand>/<model>')
def search(brand, model):
    adapter = MainParser(Car(brand=brand, model=model))
    res = adapter.parse()

    if res is None:
        return render_template('error.html', source=url_for('static', filename='ico.jpg'), error=204)

    return render_template('search.html', source=url_for('static', filename='ico.jpg'), results=res)


@app.errorhandler(404)
def error(error):
    return render_template('error.html', source=url_for('static', filename='ico.jpg'), error=error)


if __name__ == '__main__':
    app.run(debug=True)
