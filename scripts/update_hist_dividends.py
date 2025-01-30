import os
import sys
from multiprocessing import Process
sys.path.append('hyperdrive')
from DataSource import Polygon  # noqa autopep8
from Constants import CI, PathFinder  # noqa autopep8


poly = Polygon()
symbols = poly.get_symbols()
symbols = symbols[250:]


def update_poly_dividends():
    for symbol in symbols:
        filename = PathFinder().get_dividends_path(
            symbol=symbol, provider=poly.provider)
        try:
            poly.save_dividends(symbol=symbol, timeframe='max')
        except Exception as e:
            print(f'Polygon.io dividend update failed for {symbol}.')
            print(e)
        finally:
            if CI and os.path.exists(filename):
                os.remove(filename)


p1 = Process(target=update_poly_dividends)
p1.start()
p1.join()
