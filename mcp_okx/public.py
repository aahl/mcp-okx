from fastmcp import FastMCP
from pydantic import Field
from okx.PublicData import PublicAPI

from .config import *

ACCOUNT = PublicAPI(
    api_key=OKX_API_KEY,
    api_secret_key=OKX_API_SECRET,
    passphrase=OKX_PASSPHRASE,
    flag="0",
    domain=OKX_BASE_URL,
)


def add_tools(mcp: FastMCP):

    @mcp.tool(
        title="Get categories summary",
        description="Get popular cryptocurrency sections and coins",
    )
    def categories_summary(
        summaryType: str = Field("top", description="`top`/`all`"),
    ):
        api = "/priapi/v5/rubik/discover2/categories-summary"
        params = {"summaryType": summaryType, "type": "USDT"}
        return ACCOUNT._request_with_params("GET", api, params) or {}

    @mcp.tool(
        title="Get popular searches",
        description="Get popular search crypto coins",
    )
    def popular_searches():
        api = "/priapi/v5/rubik/app/public/popular-searches"
        params = {"num": 20, "rank": 0, "type": "USDT", "zone": "utc8"}
        return ACCOUNT._request_with_params("GET", api, params) or {}

    @mcp.tool(
        title="Get economic calendar data",
        description="Get the macro-economic calendar data within 3 months",
    )
    def economic_calendar():
        resp = ACCOUNT._request_with_params("GET", "/api/v5/public/economic-calendar", {}) or {}
        if resp.get("code"):
            return resp
        resp["_response_schema"] = """
        calendarId	string	Calendar ID
        date	string	Estimated release time of the value of actual field, millisecond format of Unix timestamp, e.g. 1597026383085
        region	string	Country, region or entity
        category	string	Category name
        event	string	Event name
        refDate	string	Date for which the datapoint refers to
        actual	string	The actual value of this event
        previous	string	Latest actual value of the previous period. The value will be revised if revision is applicable
        forecast	string	Average forecast among a representative group of economists
        dateSpan	string	0: The time of the event is known; 1: we only know the date of the event, the exact time of the event is unknown.
        importance	string	Level of importance. 1: low; 2: medium; 3: high
        prevInitial	string	The initial value of the previous period. Only applicable when revision happens
        ccy	string	Currency of the data
        unit	string	Unit of the data
        """
        return resp
