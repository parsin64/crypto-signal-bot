import requests
import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

BASE_URL = "https://api.bitpin.ir"
MARKET_CODE = "BTC_IRT"


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

        print("HTTP STATUS:", response.status_code)
        print("FINAL URL:", response.url)

        response.raise_for_status()

        data = response.json()

        print("\nJSON RESPONSE:")
        print(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2
            )[:20000]
        )

        return data

    except Exception as e:
        print("\nERROR:", e)
        return None


def test_markets():

    print("\n")
    print("#" * 70)
    print("# BITPIN BTC_IRT TEST")
    print("#" * 70)

    url = f"{BASE_URL}/v1/mkt/markets/"

    data = get_json(url)

    if data is None:
        return

    if isinstance(data, dict):
        markets = data.get(
            "results",
            data.get("data", [])
        )
    else:
        markets = data

    btc = None

    if isinstance(markets, list):

        for market in markets:

            if not isinstance(market, dict):
                continue

            code = str(
                market.get("code", "")
            ).upper()

            if code == MARKET_CODE:
                btc = market
                break

    print("\n")
    print("=" * 70)
    print("BTC_IRT RESULT")
    print("=" * 70)

    if btc:

        print(
            json.dumps(
                btc,
                ensure_ascii=False,
                indent=2
            )
        )

    else:

        print("BTC_IRT NOT FOUND")


def test_candle_endpoints():

    endpoints = [

        f"{BASE_URL}/v1/mkt/ohlc/{MARKET_CODE}/",

        f"{BASE_URL}/v1/mkt/candles/{MARKET_CODE}/",

        f"{BASE_URL}/v1/mkt/ohlcv/{MARKET_CODE}/",

        f"{BASE_URL}/v1/mkt/klines/{MARKET_CODE}/",

    ]

    params_list = [

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

    for endpoint in endpoints:

        for params in params_list:

            print("\n" + "-" * 70)
            print("TEST:")
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

                print("ERROR:", e)


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)
        self.send_header(
            "Content-Type",
            "text/plain; charset=utf-8"
        )
        self.end_headers()

        self.wfile.write(
            b"Bitpin API test is running."
        )

    def log_message(self, format, *args):
        return


def start_server():

    import os

    port = int(
        os.environ.get(
            "PORT",
            "10000"
        )
    )

    server = HTTPServer(
        ("0.0.0.0", port),
        Handler
    )

    print("\n")
    print("=" * 70)
    print(
        f"Test server running on port {port}"
    )
    print("=" * 70)

    server.serve_forever()


if __name__ == "__main__":

    test_markets()

    test_candle_endpoints()

    print("\n")
    print("=" * 70)
    print("BITPIN API TEST FINISHED")
    print("=" * 70)

    start_server()
