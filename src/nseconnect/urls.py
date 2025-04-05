"""
URL constants for NSE related operations
"""

# Base URLs
NSE_HOME = "https://www.nseindia.com"
NSE_MAIN = "https://www.nseindia.com"
NSE_LEGACY = "https://www.nseindia.com"

# Quote URLs
QUOTE_EQUITY_URL = f"{NSE_MAIN}/get-quotes/equity?symbol=%s"
QUOTE_API_URL = f"{NSE_MAIN}/api/quote-equity?symbol=%s"

# Stock list URLs
STOCKS_CSV_URL = f"https://archives.nseindia.com/content/equities/EQUITY_L.csv"

# Market movers URLs
TOP_GAINERS_URL = f"{NSE_MAIN}/api/live-analysis-variations?index=gainers"
TOP_LOSERS_URL = f"{NSE_MAIN}/api/live-analysis-variations?index=loosers"
TOP_FNO_GAINER_URL = f"{NSE_MAIN}/api/market-data-pre-open?key=FO"
TOP_FNO_LOSER_URL = f"{NSE_MAIN}/api/market-data-pre-open?key=FO"
FIFTYTWO_WEEK_HIGH_URL = f"{NSE_MAIN}/api/live-analysis-52Week?index=high"
FIFTYTWO_WEEK_LOW_URL = f"{NSE_MAIN}/api/live-analysis-52Week?index=low"

# Index URLs
ALL_INDICES_URL = f"{NSE_MAIN}/api/allIndices"
STOCKS_IN_INDEX_URL = f"{NSE_MAIN}/api/equity-stockIndices?index=%s"


# Historical data URLs
BHAVCOPY_BASE_URL = f"{NSE_MAIN}/archives/equities-bhavcopy/%s"
BHAVCOPY_BASE_FILENAME = "cm%s%s%sbhav.csv"

# Drivative URLs
QUOTE_DRIVATIVE_URL = f"{NSE_MAIN}/api/quote-derivative?symbol=%s"
