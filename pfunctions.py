
from flask import Flask
from pycoingecko import CoinGeckoAPI

app = Flask(__name__, static_url_path='/static')

cg = CoinGeckoAPI()
coinlist = cg.get_coins_list()

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


# ...


#Get icon variation by % value (up/upup/dw/dwdw)
def Iconvariation(argument):
    if argument >= 0 and argument < 1:
        icon_url = "/static/image/upx1.png"
    elif argument > 1:
        icon_url = "/static/image/upx2.png"
    elif argument < -1:
        icon_url = "/static/image/dwx2.png"
    elif argument > -1 and argument < 0:
        icon_url = "/static/image/dwx1.png"
    else:
        print("ERROR variation_icon_url")

    return icon_url


#https://github.com/man-c/pycoingecko
#https://www.coingecko.com/en/api/documentation
#https://stackoverflow.com/questions/4541051/parsing-dictionaries-within-dictionaries
#get API price by id
def Getprice(id):
    cgprice = cg.get_price(ids=id, vs_currencies='eur')[id]['eur']
    print(cgprice)
    return cgprice


#get currency name by id
def Getname(id):
    cgname = cg.get_coins_markets(vs_currency='eur',
                                  per_page=1,
                                  page=1,
                                  ids=id)[0]['name']
    print('cgname : ', cgname)
    return cgname


#get currency icon by id
def Geticon(id):
    cgicon = cg.get_coins_markets(vs_currency='eur',
                                  per_page=1,
                                  page=1,
                                  ids=id)[0]['image']
    print('cgicon : ', cgicon)
    return cgicon


#get currency symbol by id
def Getsymbol(id):
    cgsymbol = cg.get_coins_markets(vs_currency='eur',
                                    per_page=1,
                                    page=1,
                                    ids=id)[0]['symbol']
    print('cgsymbol : ', cgsymbol)
    return cgsymbol.upper()



