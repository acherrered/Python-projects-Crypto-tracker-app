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

#https://github.com/man-c/pycoingecko
#https://www.coingecko.com/en/api/documentation
cg = CoinGeckoAPI()
coinlist = cg.get_coins_list()

class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idcurrency = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float)
    price = db.Column(db.Float)
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
    icon_url = "/static/image/upx1.png"
   elif argument>1:
    icon_url = "/static/image/upx2.png"
   elif argument<-1:
    icon_url = "/static/image/dwx2.png"
   elif  argument>-1 and argument<0:
    icon_url = "/static/image/dwx1.png"
   else:
    print("ERROR variation_icon_url")
  
   return icon_url

#get API price by id
def Getprice(id):
  cgprice =  cg.get_price(ids=id, vs_currencies='eur')[id]['eur']
  print(cgprice)
  return cgprice

#get currency name by id
def Getname(id):
  cgname =  cg.get_coins_markets(vs_currency='eur', per_page=1, page=1, ids=id)[0]['name']
  print('cgname : ', cgname)
  return cgname

#get currency icon by id
def Geticon(id):
  cgicon =  cg.get_coins_markets(vs_currency='eur', per_page=1, page=1, ids=id)[0]['image']
  print('cgicon : ', cgicon)
  return cgicon

#get currency symbol by id
def Getsymbol(id):
  cgsymbol =  cg.get_coins_markets(vs_currency='eur', per_page=1, page=1, ids=id)[0]['symbol']
  print('cgsymbol : ', cgsymbol)
  return cgsymbol.upper()

#get total
def Total():
   total = 0
   currency = Currency.query.all()
   for transaction in currency:
      price = cg.get_price(ids=transaction.idcurrency, vs_currencies='eur')[transaction.idcurrency]['eur']
      balance = (transaction.price*transaction.quantity) - (price*transaction.quantity)
      total += balance
   return str(round(total, 2))

#print('test number : ', (float(0.001)))
  
@app.route('/')
def index():
     #table()
     float()
     #print(int(float("0.001")))
     currency = Currency.query.all()
     return render_template('index.html', currency=currency, getprice=Getprice, getname=Getname, geticon=Geticon, iconvariation=Iconvariation, valuevariation=Valuevariation, getsymbol=Getsymbol, total=Total)
 
# ...

def float():
   currency = Currency.query.all()
   for currency in currency:
      price = print ('print : ', currency.price)

   return price



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


#print('test', cg.get_coins_markets(vs_currency='eur', per_page=1, page=1, ids='bitcoin'))

item = db.session.query(Currency).filter(Currency.idcurrency=="bitcoin").first()
print ('item : ', item.id)
          
@app.route('/create/', methods=('GET', 'POST'))
def create():
  coinlist = cg.get_coins_list()
  #print(coinlist)
  if request.method == 'POST':
        idcurrency = request.form['idcurrency']
        price = (request.form['price'])
        quantity = (request.form['quantity'])
        currency = Currency(idcurrency=idcurrency,
                          price=price,
                          quantity=quantity)
        db.session.add(currency)
        db.session.commit()
                    
        return redirect(url_for('index'))
  return render_template('create.html', **locals(), coinlist=coinlist)


# ...

  # ...

@app.route('/<int:currency_id>/')
def currency(currency_id):
    currency = Currency.query.get_or_404(currency_id)
    return render_template('currency.html', currency=currency)
# ...
  

  
@app.route('/<int:currency_id>/edit/', methods=('GET', 'POST'))
def edit(currency_id):
    currency = Currency.query.get_or_404(currency_id)

    if request.method == 'POST':
        idcurrency = request.form['idcurrency']
        price = (request.form['price'])
        quantity = (request.form['quantity'])

        currency.idcurrency = idcurrency
        currency.price = price
        currency.quantity = quantity


        db.session.add(currency)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit.html', currency=currency, coinlist=coinlist)


# ...

@app.post('/<int:currency_id>/delete/')
def delete(currency_id):
    currency = Currency.query.get_or_404(currency_id)
    db.session.delete(currency)
    db.session.commit()
    return redirect(url_for('index'))


@app.post('/<currency_idcurrency>/delete_page/')
def delete_page(currency_idcurrency):
    item = db.session.query(Currency).filter(Currency.idcurrency==currency_idcurrency).first()
    currency = Currency.query.get_or_404(item.id)
    db.session.delete(currency)
    db.session.commit()
  
    return redirect(url_for('index'))
  
    return render_template('delete_page.html', xcurrency=Currency)

app.run(host='0.0.0.0', port=8080)