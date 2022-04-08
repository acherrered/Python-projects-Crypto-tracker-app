import os
from flask import Flask, render_template, request, url_for, redirect
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.sql import func
import re
from pycoingecko import CoinGeckoAPI
from apscheduler.schedulers.background import BackgroundScheduler
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64

import pfunctions
from db import db

from currency import Currency as Currency
from graph import Graph as Graph
from currency import Total
from graph import Getdate
from graph import Getvalue

app = Flask(__name__, static_url_path='/static')
db.init_app(app)
cg = CoinGeckoAPI()
coinlist = cg.get_coins_list()


#https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#Creating the Database via the model
#export FLASK_APP=main
#flask shell
#>>> from main import db, Currency
#>>> db.create_all()
#>>> Currency.query.all()
      
  
#https://stackoverflow.com/questions/21214270/how-to-schedule-a-function-to-run-every-hour-on-flask
# save the total balance one time per day 24h
def sensor():
    """ Function for test purposes. """
    print("Scheduler is alive!")

    addvalue = Graph(totalvalue=Total())
    db.session.add(addvalue)
    db.session.commit()

sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor, 'interval', minutes=1440)
sched.start()

@app.route('/')
def index():
    Getdate()
    Getvalue()
    currency = Currency.query.all()
    return render_template('index.html',
                           currency=currency,
                           getprice=pfunctions.Getprice,
                           getname=pfunctions.Getname,
                           geticon=pfunctions.Geticon,
                           iconvariation=pfunctions.Iconvariation,
                           valuevariation=pfunctions.Valuevariation,
                           getsymbol=pfunctions.Getsymbol,
                           total=Total)


# ...
# to creat a transaction
@app.route('/create/', methods=('GET', 'POST'))
def create():
    coinlist = cg.get_coins_list()

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

# to creat a page for eache transaction
@app.route('/<int:currency_id>/')
def currency(currency_id):
    currency = Currency.query.get_or_404(currency_id)
    return render_template('currency.html',
                           currency=currency,
                           getname=pfunctions.Getname,
                           getsymbol=pfunctions.Getsymbol,
                           geticon=pfunctions.Geticon)


# ...

# to edit a transaction
@app.route('/edit/', methods=('GET', 'POST'))
def edit():

    db_currency = Currency.query.all()
    item  = request.form.get('idcurrency')
   # item = db.session.query(Currency).filter(
        #Currency.idcurrency == idcurrency).first()
    print('edit : ', item)

    if request.method == 'POST':
        currency = Currency.query.get_or_404(item)
        print('edit : ', item)

        #idcurrency = request.form['idcurrency']
        price = (request.form['price'])
        quantity = (request.form['quantity'])

        #currency.idcurrency = idcurrency
        currency.price = price
        currency.quantity = quantity

        db.session.add(currency)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit.html',
                           db_currency=db_currency,
                           getsymbol=pfunctions.Getsymbol,
                           getname=pfunctions.Getname)


# ...

#to delet a transaction
  
@app.route('/delete_page/', methods=('GET', 'POST'))
def delete_page():
    xcurrency_idcurrency = request.form.get('currency_idcurrency')
    print('url id : ', xcurrency_idcurrency, type(xcurrency_idcurrency))
    parsed_currency_idcurrency = re.split('----', str(xcurrency_idcurrency))[0]
    print('url xid : ', parsed_currency_idcurrency,
          type(parsed_currency_idcurrency))
    currency = Currency.query.all()
    if request.method == 'POST':
        #https://stackoverflow.com/questions/36972044/sqlalchemy-select-id-from-table-1-where-name-xyz/36997324
        item = db.session.query(Currency).filter(
            Currency.idcurrency == parsed_currency_idcurrency).first()
        del_currency = Currency.query.get_or_404(item.id)
        db.session.delete(del_currency)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('delete_page.html',
                           currency=currency,
                           getname=pfunctions.Getname,
                           getsymbol=pfunctions.Getsymbol,
                           getprice=pfunctions.Getprice)

    

#https://stackoverflow.com/questions/20107414/passing-a-matplotlib-figure-to-html-flask
# to creat a figure with matplotlib
@app.route('/graph/')
def graph():
    img = BytesIO()
    
    #https://pythonguides.com/matplotlib-change-background-color/
    plt.figure(facecolor='black', figsize=(12,6))
    
    plt.rcParams.update({'axes.facecolor': 'black'})
    #plt.figure(figsize=(12,6)) 
    #https://stackoverflow.com/questions/9627686/plotting-dates-on-the-x-axis-with-pythons-matplotlib
    ax = plt.axes()
    #https://stackoverflow.com/questions/25689238/show-origin-axis-x-y-in-matplotlib-plot
    ax.spines['bottom'].set_position('zero')
       
    x = Getdate()
    y = Getvalue()
    
    #ax.spines['bottom'].set_color('yellow')
    plt.plot(x, y, color='green', linewidth=4.0)
    plt.gcf().autofmt_xdate()
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    
    #https://www.adamsmith.haus/python/answers/how-to-change-the-color-of-the-axes-of-a-plot-in-matplotlib-in-python
    #changing ax color
    ax.spines["bottom"].set_color("white")
    ax.spines["top"].set_color("black")
    ax.spines["left"].set_color("white")

  #https://stackoverflow.com/questions/14165344/matplotlib-coloring-axis-tick-labels
   #changing label color
    label = plt.xlabel("date",
              fontweight ='bold',
              fontsize=16,
              loc="right")
    label.set_color("white")
    label = plt.ylabel("Euro €",
              fontweight ='bold',
              fontsize=16,
              loc="center")
    label.set_color("white")
    
    #saving the figure as image
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
  
    #builing the URL of the figure
    graph_url = base64.b64encode(img.getvalue()).decode('utf8')
    print(len(graph_url))
    return render_template('graph.html', graph_url=graph_url)

    
app.run(host='0.0.0.0', port=8080)
