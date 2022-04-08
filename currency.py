from db import db
from sqlalchemy.sql import func

from flask import Flask
from pycoingecko import CoinGeckoAPI


app = Flask(__name__, static_url_path='/static')
#https://stackoverflow.com/questions/66251612/cannot-import-name-db-from-partially-initialized-module-models-most-likely
db.init_app(app)

cg = CoinGeckoAPI()
coinlist = cg.get_coins_list()


#add currency table
class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idcurrency = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float)
    price = db.Column(db.Float)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'<Currency {self.idcurrency}>'


#get total
def Total():
    total = 0
    currency = Currency.query.all()
    for transaction in currency:
        price = cg.get_price(
            ids=transaction.idcurrency,
            vs_currencies='eur')[transaction.idcurrency]['eur']
        balance = (transaction.price *
                   transaction.quantity) - (price * transaction.quantity)
        total += balance
    return str(round(total, 2))

