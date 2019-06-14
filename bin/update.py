import argparse
from app import APP
from stocks.data_access import TickerDataAccess
from stocks.models import Ticker

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--stock", help="stock symbol")
parser.add_argument("-l", "--limit", default=100, help="number of tickers to update")
parser.add_argument("-t", "--type", default="daily", help="type of ticker")
args = parser.parse_args()

APP.update(args.stock, args.type, int(args.limit))
