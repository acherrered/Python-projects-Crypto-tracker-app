from db import db
from sqlalchemy.sql import func
from flask import Flask

app = Flask(__name__, static_url_path='/static')
db.init_app(app)

# add graph table
class Graph(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    totalvalue = db.Column(db.Float)
    #totaldate = db.Column(db.Float)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'<Graph {self.totalvalue}>'


#https://stackoverflow.com/questions/37133774/how-can-i-select-only-one-column-using-sqlalchemy
def Getdate():
    dates = db.session.query(Graph.created_at)
    all_dates = dates.all()

    xdates = []
    for row in all_dates:
        xx = dict(row).values()  #
        yy = (list(xx))
        xdates += yy

    #https://stackoverflow.com/questions/10624937/convert-datetime-object-to-a-string-of-date-only-in-python
    tdate = []
    for date in xdates:
        tt = date.strftime('%d/%m/%y')
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
