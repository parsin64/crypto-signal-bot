```python
import requests
import json
from pprint import pprint

BASE_URL = "https://api.bitpin.ir"

# ---------------------------------------------------------
# تنظیمات
# ---------------------------------------------------------

MARKET_CODE = "BTC_IRT"

# ---------------------------------------------------------
# تابع درخواست
# ---------------------------------------------------------

def get_json(url, params=None):
    print("\n" + "=" * 70)
    print("REQUEST")
    print("=" * 70)

    print("URL:", url)

    if params:
        print("PARAMS:", params)

    try:
        response = requests.get(
            url,
            params=params,
            timeout=20
        )

        print("\nHTTP STATUS:", response.status_code)
        print("FINAL URL:", response.url)

        print("\nHEADERS:")
        print(response.headers)

        response.raise_for_status()

        try:
            data = response.json()
        except Exception:
            print("\nResponse is not JSON:")
            print(response.text[:5000])
            return None

        print("\nJSON RESPONSE:")
        print(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2
            )[:20000]
        )

        return data

    except requests.RequestException as e:

        print("\nREQUEST ERROR:")
        print(e)

        return None


# ---------------------------------------------------------
# 1. دریافت لیست بازارها
# ---------------------------------------------------------

print("\n")
print("#" * 70)
print("# BITPIN API TEST")
print("# MARKET:", MARKET_CODE)
print("#" * 70)

markets_url = (
    f"{BASE_URL}/v1/mkt/markets/"
)

markets = get_json(
    markets_url
)


# ---------------------------------------------------------
# پیدا کردن BTC_IRT
# ---------------------------------------------------------

btc_market = None

if isinstance(markets, dict):

    market_list = markets.get(
        "results",
        markets.get(
            "data",
            []
        )
    )

elif isinstance(markets, list):

    market_list = markets

else:

    market_list = []


for market in market_list:

    if not isinstance(market, dict):
        continue

    code = str(
        market.get("code", "")
    ).upper()

    if code == MARKET_CODE:

        btc_market = market
        break


print("\n")
print("=" * 70)
print("BTC_IRT MARKET")
print("=" * 70)

if btc_market:

    print(
        json.dumps(
            btc_market,
            ensure_ascii=False,
            indent=2
        )
    )

else:

    print(
        "BTC_IRT was not found in /v1/mkt/markets/"
    )


# ---------------------------------------------------------
# 2. آزمایش endpointهای احتمالی فقط برای کشف API
# ---------------------------------------------------------

candidate_endpoints = [

    f"{BASE_URL}/v1/mkt/ohlc/{MARKET_CODE}/",

    f"{BASE_URL}/v1/mkt/candles/{MARKET_CODE}/",

    f"{BASE_URL}/v1/mkt/ohlcv/{MARKET_CODE}/",

    f"{BASE_URL}/v1/mkt/klines/{MARKET_CODE}/",

]


params_to_try = [

    {
        "interval": "15m",
        "limit": 10
    },

    {
        "timeframe": "15m",
        "limit": 10
    },

    {
        "step": 900,
        "limit": 10
    },

]


print("\n")
print("#" * 70)
print("# CANDLE ENDPOINT DISCOVERY")
print("#" * 70)


for endpoint in candidate_endpoints:

    for params in params_to_try:

        print("\n")
        print("-" * 70)
        print("Testing:")
        print(endpoint)
        print(params)
        print("-" * 70)

        try:

            response = requests.get(
                endpoint,
                params=params,
                timeout=15
            )

            print(
                "HTTP:",
                response.status_code
            )

            print(
                "URL:",
                response.url
            )

            content_type = response.headers.get(
                "content-type",
                ""
            )

            print(
                "Content-Type:",
                content_type
            )

            if response.status_code == 200:

                try:

                    data = response.json()

                    print(
                        json.dumps(
                            data,
                            ensure_ascii=False,
                            indent=2
                        )[:10000]
                    )

                    print(
                        "\n>>> POSSIBLE WORKING ENDPOINT <<<"
                    )

                except Exception:

                    print(
                        response.text[:5000]
                    )

            else:

                print(
                    response.text[:2000]
                )

        except Exception as e:

            print(
                "ERROR:",
                e
            )


# ---------------------------------------------------------
# پایان
# ---------------------------------------------------------

print("\n")
print("=" * 70)
print("TEST FINISHED")
print("=" * 70)

print(
    """
نتیجه این تست:

1. اطلاعات کامل BTC_IRT از markets API نمایش داده شد.
2. چند endpoint احتمالی کندل بررسی شد.
3. status code و پاسخ هر endpoint نمایش داده شد.
4. اگر endpoint صحیح پیدا شود، عبارت
   POSSIBLE WORKING ENDPOINT
   نمایش داده می‌شود.

این فایل هیچ معامله‌ای انجام نمی‌دهد.
"""
)
```
