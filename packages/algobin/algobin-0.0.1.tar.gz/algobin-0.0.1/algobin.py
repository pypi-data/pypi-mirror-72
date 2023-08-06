import logging
import algoutils
import requests
from urllib.parse import urlencode
import hmac
import hashlib

BINANCE_URL = "https://api.binance.com"
KLINE_PATH = "/api/v3/klines"
TICKER_PRICE_PATH = "/api/v3/ticker/price"
SPOT_ACCOUNT_PATH = "/api/v3/account"
MARGIN_ACCOUNT_PATH = "/sapi/v1/margin/account"
MARGIN_MAX_BORROW_PATH = "/sapi/v1/margin/maxBorrowable"
SPOT_ORDER_PATH = "/api/v3/order"
MARGIN_TRANSFER_PATH = "/sapi/v1/margin/transfer"
MARGIN_BORROW_PATH = "/sapi/v1/margin/loan"
MARGIN_ORDER_PATH = "/sapi/v1/margin/order"
MARGIN_REPAY_PATH = "/sapi/v1/margin/repay"

# Data related functions
def get_kline(symbol, interval):
    """Getting market data from binance public api

    Arguments:
        symbol {string} -- market symbol
        interval {string} -- data interval

    Returns:
        list -- a list of dictionaries contains market data
    """
    params = {"symbol": symbol, "interval": interval}
    try:
        response = requests.get(url=BINANCE_URL + KLINE_PATH, params=params)
        response.raise_for_status()
        kline = response.json()
        kline = kline[:-1]
        return kline
    except requests.exceptions.RequestException as err:
        logging.error(err)
        return None

def get_ticker_price(symbol):
    """Gets ticker price of given symbol

    Arguments:
        symbol {string} -- symbol

    Returns:
        float -- ticker price of given symbol
    """
    params = {"symbol": symbol}

    try:
        response = requests.get(url=BINANCE_URL + TICKER_PRICE_PATH, params=params)
        response.raise_for_status()
        data = response.json()
        return float(data["price"])
    except requests.exceptions.HTTPError as err:
        logging.error(err)
        return None

def get_spot_balance(asset, API_KEY, SECRET):
    """Function gets spot account balance for given asset

    Arguments:
        asset {string} -- Name of asset

    Returns:
        string -- balance of given asset
    """
    timestamp = algoutils.get_current_timestamp()

    params = {"timestamp": timestamp, "recvWindow": 5000}
    query_string = urlencode(params)
    params["signature"] = hmac.new(SECRET.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()

    headers = {"X-MBX-APIKEY": API_KEY}

    try:
        response = requests.get(url=BINANCE_URL + SPOT_ACCOUNT_PATH, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        for _, balance in enumerate(data["balances"]):
            if balance["asset"] == asset:
                return float(balance["free"])
    except requests.exceptions.RequestException as err:
        logging.error(err)
        return None

def get_margin_balance(asset, API_KEY, SECRET):
    """Function gets margin account balance for given asset

    Arguments:
        asset {string} -- Name of asset

    Returns:
        string -- balance of given asset
    """
    timestamp = algoutils.get_current_timestamp()

    params = {"timestamp": timestamp, "recvWindow": 5000}
    query_string = urlencode(params)
    params["signature"] = hmac.new(SECRET.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()

    headers = {"X-MBX-APIKEY": API_KEY}

    try:
        response = requests.get(url=BINANCE_URL + MARGIN_ACCOUNT_PATH, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        for _, balance in enumerate(data["userAssets"]):
            if balance["asset"] == asset:
                logging.info(balance)
                return float(balance["netAsset"])
    except requests.exceptions.RequestException as err:
        logging.error(err)
        return None

def get_margin_free_balance(asset, API_KEY, SECRET):
    """Function gets margin account debt for given asset

    Arguments:
        asset {string} -- Name of asset

    Returns:
        float -- debt of given asset
    """
    timestamp = algoutils.get_current_timestamp()

    params = {"timestamp": timestamp, "recvWindow": 5000}
    query_string = urlencode(params)
    params["signature"] = hmac.new(SECRET.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()

    headers = {"X-MBX-APIKEY": API_KEY}

    try:
        response = requests.get(url=BINANCE_URL + MARGIN_ACCOUNT_PATH, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        for _, balance in enumerate(data["userAssets"]):
            if balance["asset"] == asset:
                logging.info(balance)
                return float(balance["free"])
    except requests.exceptions.RequestException as err:
        logging.error(err)
        return None


def get_margin_debt(asset, API_KEY, SECRET):
    """Function gets margin account debt for given asset

    Arguments:
        asset {string} -- Name of asset

    Returns:
        float -- debt of given asset
    """
    timestamp = algoutils.get_current_timestamp()

    params = {"timestamp": timestamp, "recvWindow": 5000}
    query_string = urlencode(params)
    params["signature"] = hmac.new(SECRET.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()

    headers = {"X-MBX-APIKEY": API_KEY}

    try:
        response = requests.get(url=BINANCE_URL + MARGIN_ACCOUNT_PATH, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        for _, balance in enumerate(data["userAssets"]):
            if balance["asset"] == asset:
                logging.info(balance)
                return float(balance["borrowed"]) + float(balance["interest"])
    except requests.exceptions.RequestException as err:
        logging.error(err)
        return None

def get_max_borrowable(asset, API_KEY, SECRET):
    """Function gets max borrowable amount for given asset

    Arguments:
        asset {string} -- Name of asset

    Returns:
        string -- max borrowable amount of given asset
    """
    timestamp = algoutils.get_current_timestamp()

    params = {"asset": asset, "timestamp": timestamp, "recvWindow": 5000}
    query_string = urlencode(params)
    params["signature"] = hmac.new(SECRET.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()

    headers = {"X-MBX-APIKEY": API_KEY}

    try:
        response = requests.get(url=BINANCE_URL + MARGIN_MAX_BORROW_PATH, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        return data["amount"]
    except requests.exceptions.RequestException as err:
        logging.error(err)
        return None

# Indicator related functions
def get_ohlc(kline):
    """Creates open, high, low, close data from kline

    Arguments:
        kline {list} -- kline data

    Returns:
        list -- lists of open, high, low, close data
    """
    opn = [float(o[1]) for o in kline]
    close = [float(d[4]) for d in kline]
    high = [float(h[2]) for h in kline]
    low = [float(l[3]) for l in kline]

    return opn, high, low, close

# Spot account trade functions
def spot_order(symbol, side, type, quantity, API_KEY, SECRET):
    """Triggers an order for spot account with given parameters

    Arguments:
        symbol {string} -- symbol
        side {string} -- side of order
        type {string} -- type of order
        quantity {float} -- quantity of order

    Returns:
        string-- json response of order
    """
    timestamp = algoutils.get_current_timestamp()

    params = {"symbol": symbol, "side": side, "type": type, "quantity": quantity, "timestamp": timestamp, "recvWindow": 5000}
    query_string = urlencode(params)
    params["signature"] = hmac.new(SECRET.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()

    headers = {"X-MBX-APIKEY": API_KEY}

    try:
        response = requests.post(url=BINANCE_URL + SPOT_ORDER_PATH, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as err:
        logging.error(err)
        return None

# Margin account trade functions
def margin_transfer(asset, amount, side, API_KEY, SECRET):
    """Making asset transfer from spot account to margin account or vice versa

    Arguments:
        asset {string} -- asset to transfer
        amount {float} -- amount of asset to transfer
        side {int} -- side of transfer. 1 for spot to margin account, 2 for margin to spot account

    Returns:
        string -- json response of transfer operation
    """
    timestamp = algoutils.get_current_timestamp()
    params = {"asset": asset, "amount": amount, "type": side, "recvWindow": 5000, "timestamp": timestamp}
    query_string = urlencode(params)
    params["signature"] = hmac.new(SECRET.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()

    headers = {"X-MBX-APIKEY": API_KEY}

    try:
        response = requests.post(url=BINANCE_URL + MARGIN_TRANSFER_PATH, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as err:
        logging.error(err)
        return None

def margin_borrow(asset, amount, API_KEY, SECRET):
    """Borrows asset from market

    Arguments:
        asset {string} -- asset to borrow
        amount {float} -- amount of asset

    Returns:
        string -- json response of borrow operation
    """
    timestamp = algoutils.get_current_timestamp()

    params = {"asset": asset, "amount": amount, "recvWindow": 5000, "timestamp": timestamp}
    query_string = urlencode(params)
    params["signature"] = hmac.new(SECRET.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()

    headers = {"X-MBX-APIKEY": API_KEY}

    try:
        response = requests.post(url=BINANCE_URL + MARGIN_BORROW_PATH, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as err:
        logging.error(err)
        return None

def margin_order(symbol, side, type, quantity, API_KEY, SECRET):
    """Triggers an order for margin account with given parameters

    Arguments:
        symbol {string} -- symbol
        side {string} -- side of order
        type {string} -- type of order
        quantity {float} -- quantity of order

    Returns:
        string-- json response of order
    """
    timestamp = algoutils.get_current_timestamp()

    params = {"symbol": symbol, "side": side, "type": type, "quantity": quantity, "timestamp": timestamp, "recvWindow": 5000}
    query_string = urlencode(params)
    params["signature"] = hmac.new(SECRET.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()

    headers = {"X-MBX-APIKEY": API_KEY}

    try:
        response = requests.post(url=BINANCE_URL + MARGIN_ORDER_PATH, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as err:
        logging.error(err)
        return None

def margin_repay(asset, amount, API_KEY, SECRET):
    """Repays margin account liability

    Arguments:
        asset {string} -- asset
        amount {float} -- amount to repay

    Returns:
        string -- json response of repay operation
    """
    timestamp = algoutils.get_current_timestamp()

    params = {"asset": asset, "amount": amount, "recvWindow": 5000, "timestamp": timestamp}
    query_string = urlencode(params)
    params["signature"] = hmac.new(SECRET.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()

    headers = {"X-MBX-APIKEY": API_KEY}

    try:
        response = requests.post(url=BINANCE_URL + MARGIN_REPAY_PATH, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as err:
        logging.error(err)
        return None
