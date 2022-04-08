import unittest
from main import app
import re
import pfunctions

#$ python test_utils.py
#from replit you have to disable the last line in main.py that to give access to unit tests #app.run(host='0.0.0.0', port=8080)

class main(unittest.TestCase):


    def test_routeCurrency(self):
     adapter = app.url_map.bind('')
     # This raise werkzeug.exceptions.NotFound.
     adapter.match('/4/')

    def test_delete_pageRoute(self):
     adapter = app.url_map.bind('')
     # This raise werkzeug.exceptions.NotFound.
     adapter.match('/delete_page/')

    def test_indexRoute(self):
     adapter = app.url_map.bind('')
     # This raise werkzeug.exceptions.NotFound.
     adapter.match('/')

    def test_creatRout(self):
     adapter = app.url_map.bind('')
    # This raise werkzeug.exceptions.NotFound.
     adapter.match('/create/')

    def test_editRoute(self):
     adapter = app.url_map.bind('')
   # This raise werkzeug.exceptions.NotFound.
     adapter.match('/edit/')

    def test_graphRoute(self):
     adapter = app.url_map.bind('')
     # This raise werkzeug.exceptions.NotFound.
     adapter.match('/graph/')

    def test_urlVariation(self):
     urlVariation = pfunctions.Iconvariation(0)
     match = re.findall("upx1.png", urlVariation)
     self.assertEquals(match[0], "upx1.png")

    def test_currencyIcon(self):
     iconUrl = str(pfunctions.Geticon('bitcoin'))
     match = re.findall("bitcoin.png", iconUrl)
     self.assertEquals(match[0], 'bitcoin.png')

    def test_currencySymbol(self):
     self.assertEquals(pfunctions.Getsymbol('bitcoin'), 'BTC')

    def test_price_variation(self):
     self.assertEquals(pfunctions.Valuevariation(100, 110), 10)

    def test_currencyName(self):
     self.assertEquals(pfunctions.Getname('bitcoin'), 'Bitcoin')

if __name__ == '__main__':
        unittest.main()