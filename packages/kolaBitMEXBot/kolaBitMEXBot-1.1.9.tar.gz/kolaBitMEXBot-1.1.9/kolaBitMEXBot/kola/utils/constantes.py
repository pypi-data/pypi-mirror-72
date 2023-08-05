# -*- coding: utf-8 -*-
"""Constantes"""

# some default cols
EXECOLS = [
    "orderID",
    "clOrdID",
    "side",
    "orderQty",
    "price",
    "stopPx",
    "execType",
    "ordType",
    "execInst",
    "ordStatus",
    "triggered",
    "transactTime",
]

EXECOLS_L = EXECOLS + ["lastQty", "lastPx", "lastMkt", "commission"]

# to get price in bargain.price
SETTLEMENTPRICES = {"XBTUSD": ".BXBT", "ADAM20": ".BADAXBT30M"}

# used to round price before passing orders
PRICE_PRECISION = {"XBTUSD": 0.5, "ADAM20": 1e-8}

# used in condition
PRICELIST_DFT = [
    "IndexPrice",
    "LastPrice",
    "MarkPrice",
    "askPrice",
    "bidPrice",
    "lastMidPrice",
]

INSTRUMENT_PRICES = [
    f"{suf}Price"
    for suf in [
        "max",
        "prevClose",
        "prev",
        "high",
        "low",
        "last",
        "bid",
        "mid",
        "ask",
        "impactBid",
        "impactMid",
        "impactAsk",
        "fair",
        "mark",
        "indicativeSettle",
    ]
] + ["lastPriceProtected"]


# price variation in % to reach to short to the maximun the tail (stop)
# used to set a e^-f(t) fonction controling the tail's size.
MAX_PRICE_VARIATION = {"XBTUSD": 2.6, "ADAM20": 2.6}
