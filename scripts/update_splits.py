import os
import sys
from multiprocessing import Process, Value
sys.path.append('hyperdrive')
from DataSource import Polygon  # noqa autopep8
from Constants import PathFinder  # noqa autopep8
import Constants as C  # noqa autopep8

counter = Value('i', 0)
poly = Polygon()
symbols = poly.get_symbols()


def update_poly_splits():
    for symbol in symbols:
        try:
            filename = poly.save_splits(
                symbol=symbol, timeframe='3m',
                retries=1 if C.TEST else C.DEFAULT_RETRIES)
            with counter.get_lock():
                counter.value += 1
        except Exception as e:
            print(f'Polygon.io split update failed for {symbol}.')
            print(e)
        finally:
            filename = PathFinder().get_splits_path(
                symbol=symbol, provider=poly.provider)
            if C.CI and os.path.exists(filename):
                os.remove(filename)


p1 = Process(target=update_poly_splits)
p1.start()
p1.join()

if counter.value / len(symbols) < 0.05:
    exit(1)
