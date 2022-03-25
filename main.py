import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from pycoingecko import CoinGeckoAPI

basedir = os.path.abspath(os.path.dirname(__file__))

#https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application

#
app = Flask(__name__, static_url_path='/static')

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
cg = CoinGeckoAPI()

class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idcurrency = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
   
    def __repr__(self):
        return f'<Currency {self.idcurrency}>'

#Creating the Database via the model
  #>>> export FLASK_APP=main
  #>>> flask shell
  #>>> from main import db, Currency
  #>>> db.create_all()

# ...

#get % value of variation between two values
def Valuevariation(first, second):
    diff = second - first
    change = 0
    try:
        if diff > 0:
            change = (diff / first) * 100
        elif diff < 0:
            diff = first - second
            change = -((diff / first) * 100)
    except ZeroDivisionError:
        return float('inf')
    return change
  
#Get icon variation by % value (up/upup/dw/dwdw)
def Iconvariation(argument):
   if argument>=0 and argument<1:
    icon_url = "icon1"
   elif argument>1:
    icon_url = "icon2"
   elif argument<-1:
    icon_url = "icon3"
   elif  argument>-1 and argument<0:
    icon_url = "icon4"
   else:
    print("variation_icon_url")
  
   return icon_url

#get real price by id
def Getprice(id):
  cgprice =  cg.get_price(ids=id, vs_currencies='eur')[id]['eur']
  print(cgprice)
  return cgprice

#get name by id
def Getname(id):
  cgname =  cg.get_coins_markets(vs_currency='eur', per_page=1, page=1, ids=id)[0]['name']
  print('cgname : ', cgname)
  return cgname

#get icon by id
def Geticon(id):
  cgicon =  cg.get_coins_markets(vs_currency='eur', per_page=1, page=1, ids=id)[0]['image']
  print('cgicon : ', cgicon)
  return cgicon

#get symbol by id
def Getsymbol(id):
  cgsymbol =  cg.get_coins_markets(vs_currency='eur', per_page=1, page=1, ids=id)[0]['symbol']
  print('cgsymbol : ', cgsymbol)
  return cgsymbol


  
@app.route('/')
def index():
     table()
     currency = Currency.query.all()
     return render_template('index.html', currency=currency, getprice=Getprice, getname=Getname, geticon=Geticon, iconvariation=Iconvariation, valuevariation=Valuevariation, getsymbol=Getsymbol)
 
# ...

def table():  
    total = 0
    currency = Currency.query.all()
    for transaction in currency:
     print(transaction.idcurrency)
     print('price', transaction.price)
     print(transaction.quantity)
     price = cg.get_price(ids=transaction.idcurrency, vs_currencies='eur')[transaction.idcurrency]['eur']
     print('actual price : ', price)
     name = cg.get_coins_markets(vs_currency='eur', per_page=1, page=1, ids=(transaction.idcurrency))[0]['name']
     print('name : ', name)
     currencyicon = cg.get_coins_markets(vs_currency='eur', per_page=1, page=1, ids=(transaction.idcurrency))[0]['image']
     print(currencyicon)
     balance = (transaction.price*transaction.quantity) - (price*transaction.quantity)
     print('balance : ', balance)
     total += balance
     print(total)
     variation = Valuevariation(price, transaction.price)
     print('change', variation)
     variation_icon_url = Iconvariation(variation)
     print(variation_icon_url)
     Getname(transaction.idcurrency)
     Geticon(transaction.idcurrency)
     Getsymbol(transaction.idcurrency)
     return render_template('create.html', **locals())
    #print(f"<id={transaction.id}, username={transaction.idcurrency}>")


print('test', cg.get_coins_markets(vs_currency='eur', per_page=1, page=1, ids='bitcoin'))

          
@app.route('/create/', methods=('GET', 'POST'))
def create():
  coinlist = cg.get_coins_list()
  #print(coinlist)
  if request.method == 'POST':
        idcurrency = request.form['idcurrency']
        price = int(request.form['price'])
        quantity = int(request.form['quantity'])
        currency = Currency(idcurrency=idcurrency,
                          price=price,
                          quantity=quantity)
        db.session.add(currency)
        db.session.commit()
                    
        return redirect(url_for('index'))
  return render_template('create.html', **locals())


# ...



app.run(host='0.0.0.0', port=8080)