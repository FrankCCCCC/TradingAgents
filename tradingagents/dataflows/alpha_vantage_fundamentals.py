import json

from .alpha_vantage_common import _make_api_request

# Limit the number of reports returned to avoid exceeding LLM token limits.
# Alpha Vantage returns ALL historical reports which can be 100K+ tokens.
MAX_ANNUAL_REPORTS = 2
MAX_QUARTERLY_REPORTS = 4


def _trim_financial_reports(response_text: str) -> str:
    """Trim financial statement JSON to only include recent reports.

    Alpha Vantage returns all historical annual and quarterly reports,
    which can exceed LLM token limits (e.g. 115K tokens for a single ticker).
    This trims to the most recent reports only.
    """
    try:
        data = json.loads(response_text)
    except (json.JSONDecodeError, TypeError):
        return response_text

    if "annualReports" in data:
        data["annualReports"] = data["annualReports"][:MAX_ANNUAL_REPORTS]
    if "quarterlyReports" in data:
        data["quarterlyReports"] = data["quarterlyReports"][:MAX_QUARTERLY_REPORTS]

    return json.dumps(data, indent=2)


def get_fundamentals(ticker: str, curr_date: str = None) -> str:
    """
    Retrieve comprehensive fundamental data for a given ticker symbol using Alpha Vantage.

    Args:
        ticker (str): Ticker symbol of the company
        curr_date (str): Current date you are trading at, yyyy-mm-dd (not used for Alpha Vantage)

    Returns:
        str: Company overview data including financial ratios and key metrics
    """
    params = {
        "symbol": ticker,
    }

    return _make_api_request("OVERVIEW", params)


def get_balance_sheet(ticker: str, freq: str = "quarterly", curr_date: str = None) -> str:
    """
    Retrieve balance sheet data for a given ticker symbol using Alpha Vantage.

    Args:
        ticker (str): Ticker symbol of the company
        freq (str): Reporting frequency: annual/quarterly (default quarterly) - not used for Alpha Vantage
        curr_date (str): Current date you are trading at, yyyy-mm-dd (not used for Alpha Vantage)

    Returns:
        str: Balance sheet data with normalized fields
    """
    params = {
        "symbol": ticker,
    }

    return _trim_financial_reports(_make_api_request("BALANCE_SHEET", params))


def get_cashflow(ticker: str, freq: str = "quarterly", curr_date: str = None) -> str:
    """
    Retrieve cash flow statement data for a given ticker symbol using Alpha Vantage.

    Args:
        ticker (str): Ticker symbol of the company
        freq (str): Reporting frequency: annual/quarterly (default quarterly) - not used for Alpha Vantage
        curr_date (str): Current date you are trading at, yyyy-mm-dd (not used for Alpha Vantage)

    Returns:
        str: Cash flow statement data with normalized fields
    """
    params = {
        "symbol": ticker,
    }

    return _trim_financial_reports(_make_api_request("CASH_FLOW", params))


def get_income_statement(ticker: str, freq: str = "quarterly", curr_date: str = None) -> str:
    """
    Retrieve income statement data for a given ticker symbol using Alpha Vantage.

    Args:
        ticker (str): Ticker symbol of the company
        freq (str): Reporting frequency: annual/quarterly (default quarterly) - not used for Alpha Vantage
        curr_date (str): Current date you are trading at, yyyy-mm-dd (not used for Alpha Vantage)

    Returns:
        str: Income statement data with normalized fields
    """
    params = {
        "symbol": ticker,
    }

    return _trim_financial_reports(_make_api_request("INCOME_STATEMENT", params))
