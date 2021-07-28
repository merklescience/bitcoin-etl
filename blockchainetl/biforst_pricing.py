# MIT License
#
# Copyright (c) 2019 Nirmal AK, nirmal@merklescience.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import requests
from datetime import datetime
from urllib3.util import Retry
from requests.adapters import HTTPAdapter

BIFRSOT_AUTH = os.getenv("BIFROST_AUTH", "")


class BifrostRequestException(Exception):
    pass


def _make_request(
        from_currency_code: str,
        to_currency_code: str,
        execution_date: str,
        access_token: str,

) -> requests.Response:
    base_url = f"https://dev.bifrost.palantree.com/coin-price-service/historical-daily-price/"
    retries = Retry(backoff_factor=5, total=5)
    adapter = HTTPAdapter(max_retries=retries)
    session = requests.Session()
    session.mount('https://', adapter)
    session.mount('http://', adapter)
    retries.BACKOFF_MAX = 600
    params = {
        "fsyms": from_currency_code,
        "tsyms": to_currency_code,
        "access_token": access_token,
        "execution_date": execution_date
    }
    return session.get(base_url, params=params)


def get_coin_price(
        from_currency_code: str,
        execution_date: datetime.date,
        to_currency_code: str = "USD",
        access_token: str = BIFRSOT_AUTH,
):
    """
    Prices are retrieved from biforst historical daily service. Please note that only historical prices are available
    only at daily average and not on hourly. We can only get latest hourly price from bifrost which won't make sense
    for daily processing hence not implemented here as compared to cryptocompare api.


    This function will throw error as this will be mostly running for daily etls where in if ETL fails we can
        rerun easily and exponential backoff and retries have been enabled for this method and at dag level
    """
    execution_date = str(datetime.fromtimestamp(execution_date).date())
    response = _make_request(
        from_currency_code=from_currency_code,
        to_currency_code=to_currency_code,
        execution_date=execution_date,
        access_token=access_token
    )
    if not response.status_code == 200:
        raise BifrostRequestException
    payload = response.json()

    if payload.get("detail", "") != "":
        raise BifrostRequestException(payload.get("detail", ""))
    if len(payload.get("historical-daily-price", [])) == 0:
        raise BifrostRequestException("Empty response from Bifrost")
    if len(payload.get("historical-daily-price", [])) > 1:
        raise BifrostRequestException("More than 1 response received from Bifrost")
    try:
        price_data = payload.get("historical-daily-price", [])[0]
        print(price_data)
    except IndexError as e:
        raise IndexError(e)
    if price_data.get("execution_timestamp", "") != execution_date:
        raise BifrostRequestException(
            f"Execution date received from bifrost {price_data.get('execution_timestamp', '')}"
            f" is different than requested for {execution_date}", )
    if price_data.get("price", None) is None:
        raise BifrostRequestException("Received None price from Bifrost")

    return round(price_data.get("price", 0), 8)

# Keeping it for future debugging, can remove if needed
# if __name__ == '__main__':
#     print("finla ", get_coin_price('BTC', 1626912002))
