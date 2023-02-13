import datetime
import requests

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = "GBT0OSG8WZ453JN"

def fortnight_report(stock_code):
    # ---------- FORTNIGHTLY REPORT ----------#
    # ----- FIND DATE -----#
    current_date = datetime.datetime.now().strftime("%d")
    current_month = datetime.datetime.now().strftime("%m")
    current_year = datetime.datetime.now().strftime("%Y")
    # ----- CHECK CURRENT DATE -----#
    if current_date == 16:

        STOCK_PARAMETERS = {
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": stock_code,
            "apikey": STOCK_API_KEY
        }

        response = requests.get(STOCK_ENDPOINT, params=STOCK_PARAMETERS)
        stock_data = response.json()
        stock_data_daily = stock_data["Time Series (Daily)"]

        # ----- VARIABLES -----#
        first_15 = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", ]
        fortnight_high = 0
        fortnight_low = 5000
        fortnight_close_high = 0
        fortnight_close_low = 5000
        fortnight_open = 0
        fortnight_close = 1
        fortnight_div = 0

        # ----- DIV AMOUNT -----#
        STOCK_OVERVIEW_PARAMS = {
            "function": "OVERVIEW",
            "symbol": stock_code,
            "apikey": STOCK_API_KEY
        }

        response = requests.get(STOCK_ENDPOINT, params=STOCK_OVERVIEW_PARAMS)
        report_overview = response.json()

        overview_list = [value for (key, value) in report_overview.items()]
        company_div_amount = float((overview_list[18]))

        for num in first_15:
            try:
                # ----- OPEN & CLOSE PRICE -----#
                fortnight_data = stock_data_daily[f"{current_year}-{current_month}-{num}"]
                if fortnight_open == 0:
                    fortnight_open += float(fortnight_data["1. open"])
                fortnight_close = float(fortnight_data["4. close"])

                # ----- HIGHEST & LOWEST CLOSE -----#
                if float(fortnight_data["4. close"]) > fortnight_close_high:
                    fortnight_close_high = float(fortnight_data["4. close"])

                if float(fortnight_data["4. close"]) < fortnight_close_low:
                    fortnight_close_low = float(fortnight_data["4. close"])

                # ----- HIGH & LOW -----#
                if float(fortnight_data["2. high"]) > fortnight_high:
                    fortnight_high = float(fortnight_data["2. high"])

                if float(fortnight_data["3. low"]) < fortnight_low:
                    fortnight_low = float(fortnight_data["3. low"])

                # ----- DIV PAYMENT -----#
                if fortnight_data["7. dividend amount"] != "0.0000":
                    fortnight_div = float(fortnight_data["7. dividend amount"])

            except KeyError:
                continue

        fortnight_price_diff = round(((fortnight_close - fortnight_open) / fortnight_open) * 100, 2)
        fortnight_close_div_yield_percent = round(100 * company_div_amount / fortnight_close, 2)
        fortnight_open_div_yield_percent = round(100 * company_div_amount / fortnight_open, 2)

        message = f"Fortnightly report for {stock_code}\n\n" \
                  f"Hey Eddie\n\n" \
                  f"Here's your report:\n\n" \
                  f"Share prices opened at ${fortnight_open} and closed for the mid month period at ${fortnight_close}.\n" \
                  f"This is a difference of {fortnight_price_diff}%\n\n" \
                  f"The highest close over the period was ${fortnight_close_high}, while the lowest close was ${fortnight_close_low}.\n\n" \
                  f"{stock_code} reached ${fortnight_high} at it's highest, and ${fortnight_low} at it's lowest this period.\n\n" \
                  f"The dividend payment during this period was ${fortnight_div} per share\n" \
                  f"The current dividend yield is {fortnight_close_div_yield_percent}% and it started the period at {fortnight_open_div_yield_percent}%."

        encoded_message = message.encode("utf-8")
        return message
