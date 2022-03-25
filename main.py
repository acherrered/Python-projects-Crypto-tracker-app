import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

from pycoingecko import CoinGeckoAPI
from apscheduler.schedulers.background import BackgroundScheduler
import datetime as dt

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64


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

class Graph(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    totalvalue = db.Column(db.Float)
    #totaldate = db.Column(db.Float)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
   
    def __repr__(self):
        return f'<Graph {self.totalvalue}>'
      
#Creating the Database via the model
  #export FLASK_APP=main
  #flask shell
  #>>> from main import db, Currency
  #>>> db.create_all()
  #>>> Currency.query.all()
  # print(01coin.id)
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

#https://stackoverflow.com/questions/4541051/parsing-dictionaries-within-dictionaries
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

#def test():
  #graph = Graph.query.all()
  #for graph in graph:
     #ygraph =  print (' Graph data : ', graph.totalvalue, graph.created_at)
  #return ygraph

#https://stackoverflow.com/questions/37133774/how-can-i-select-only-one-column-using-sqlalchemy
def Getdate():
    dates = db.session.query(Graph.created_at)
    all_dates = dates.all()
  
    #for date in all_dates:
      # xx = date #[date.strftime(d,'%d/%m/%Y').date()]
    xdates = []
    for row in all_dates:
       xx = dict(row).values()#
       yy = (list(xx))
       #x = [dt.datetime.strptimetime(d,'%m/%d/%Y').date() for d in xx]
       xdates += yy

    tdate = []
    for date in xdates:  
       tt = date.strftime('%d/%m/%Y')
       print('tt : ', tt, type(tt))
       tdate.append(tt)
      
    return tdate

def Getvalue():
    values = db.session.query(Graph.totalvalue)
    all_values = values.all()
    values = []
    for row in all_values:
      xx = dict(row)['totalvalue']
      values.append(xx)
    return values

def sensor():
    """ Function for test purposes. """
    print("Scheduler is alive!")

    addvalue = Graph(totalvalue=Total())
    db.session.add(addvalue)
    db.session.commit()

  
sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor,'interval',seconds=2000)
sched.start()
  

@app.route('/')
def index():
     #table()
   #  float()
     #print(int(float("0.001")))
     #byID = cg.get_coin_by_id("bitcoin")
     #print('byID : ', byID)
     #test()
     Getdate()
     Getvalue()
     currency = Currency.query.all()
     return render_template('index.html', currency=currency, getprice=Getprice, getname=Getname, geticon=Geticon, iconvariation=Iconvariation, valuevariation=Valuevariation, getsymbol=Getsymbol, total=Total)
 
# ...

#def float():
  # currency = Currency.query.all()
  # for currency in currency:
   #   if currency.price > 0:
    #      print(' check : ',currency.price)
    #      price = print ('print : ', currency.price)

  # return price



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

#item = db.session.query(Currency).filter(Currency.idcurrency=="bitcoin").first()
#print ('item : ', item.id)
          
@app.route('/create/', methods=('GET', 'POST'))
def create():
   coinlist = cg.get_coins_list()
   #print(coinlist)
   #Data = request.args.get('xdataid')
   #print('data : ', Data)
   #request.form.get('xdataid')
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
     
   return render_template('create.html', **locals())


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


@app.route('/delete_page/', methods=('GET','POST'))
def delete_page():
    xcurrency_idcurrency = request.form.get('currency_idcurrency')
    print ('url id : ', xcurrency_idcurrency)
    currency = Currency.query.all()
    if request.method == 'POST':
  #https://stackoverflow.com/questions/36972044/sqlalchemy-select-id-from-table-1-where-name-xyz/36997324
         item = db.session.query(Currency).filter(Currency.idcurrency==xcurrency_idcurrency).first()
         del_currency = Currency.query.get_or_404(item.id)
         db.session.delete(del_currency)
         db.session.commit()
  
    #return redirect(url_for('index'))
  
    return render_template('delete_page.html', currency=currency)

  
#https://stackoverflow.com/questions/20107414/passing-a-matplotlib-figure-to-html-flask
@app.route('/graph')
def graph():
        img = BytesIO()
        plt.figure(figsize=(12,6))
        y =  [-3,-2,-1,0,1] #Getvalue()
        x =  [0,2,1,3,4] #Getdate()
        print(type(x), x, type(y),y)
        plt.plot(x,y, c='green')
        plt.xlabel('date')
        plt.ylabel('Euro €')
        
        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode('utf8')

        return render_template('graph.html', graph_url=graph_url)

app.run(host='0.0.0.0', port=8080)