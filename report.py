import requests

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = "GBT0OSG8WZ453JN"

def initial_report(stock_code):
    #---------- INITIAL REPORT ----------#
    #-----LAST CLOSE DATA -----#
    STOCK_PARAMETERS = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": stock_code,
        "apikey": STOCK_API_KEY
    }

    response = requests.get(STOCK_ENDPOINT, params=STOCK_PARAMETERS)
    report_data = response.json()
    report_data_daily = report_data["Time Series (Daily)"]

    report_data_list = [value for (key, value) in report_data_daily.items()]
    report_yday_close = float(report_data_list[0]["4. close"])


    #-----OVERVIEW DATA -----#
    STOCK_OVERVIEW_PARAMS = {
        "function": "OVERVIEW",
        "symbol": stock_code,
        "apikey": STOCK_API_KEY
    }

    response = requests.get(STOCK_ENDPOINT, params=STOCK_OVERVIEW_PARAMS)
    report_overview = response.json()

    overview_list = [value for (key, value) in report_overview.items()]
    company_name = (overview_list[2])
    company_description = (overview_list[3])
    company_exchange = (overview_list[5])
    company_currency = (overview_list[6])
    company_country = (overview_list[7])
    company_sector = (overview_list[8])
    company_industry = (overview_list[9])
    company_address = (overview_list[10])
    company_div_amount = float((overview_list[18]))
    company_div_percent = float((overview_list[19])) * 100
    company_52_high = (overview_list[39])
    company_52_low = (overview_list[40])
    company_div_date = (overview_list[44])

    overview_message_div = (f"\n{company_name} last closed trading at ${report_yday_close}\n"
                            f"Sector: {company_sector}\n"
                            f"Industry: {company_industry}\n"
                            f"Based at: {company_address}\n"
                            f"in: {company_country}\n"
                            f"using: {company_currency}\n"
                            f"Listed on: {company_exchange}\n"
                            f"The 52-week high for {company_name} is: ${company_52_high}\n"
                            f"The 52-week low for {company_name} is: ${company_52_low}\n"
                            f"The yearly dividend amount is: {company_div_amount}{company_currency}\n"
                            f"Yearly dividend yield: {company_div_percent}%\n"
                            f"Last dividend paid on {company_div_date}\n\n"
                            f"Description: {company_description}\n"
                            )

    overview_message_no_div = (f"\n{company_name} last closed trading at ${report_yday_close}\n"
                               f"Sector: {company_sector}\n"
                               f"Industry: {company_industry}\n"
                               f"Based at: {company_address}\n"
                               f"in: {company_country}\n"
                               f"using: {company_currency}\n"
                               f"Listed on: {company_exchange}\n"
                               f"The 52-week high for {company_name} is: ${company_52_high}\n"
                               f"The 52-week low for {company_name} is: ${company_52_low}\n"
                               f"{company_name} has no dividend information available.\n\n"
                               f"Description: {company_description}\n"
                               )

    #-----WEEKLY DATA -----#
    WEEKLY_PARAMS = {
        "function": "TIME_SERIES_WEEKLY",
        "symbol": stock_code,
        "apikey": STOCK_API_KEY
    }

    response = requests.get(STOCK_ENDPOINT, params=WEEKLY_PARAMS)
    weekly_data = response.json()["Weekly Time Series"]
    week_ending = (str(weekly_data).split(":")[0]).split("'")[1]

    weekly_data_list = [value for (key, value) in weekly_data.items()]
    last_week_open = weekly_data_list[0]["1. open"]
    last_week_close = weekly_data_list[0]["4. close"]
    last_week_percent = round((float(last_week_close) - float(last_week_open)) * 100 / float(last_week_open), 2)
    last_week_high = weekly_data_list[0]["2. high"]
    last_week_low = weekly_data_list[0]["3. low"]

    weekly_data_message = (f"\nDATA FOR WEEK ENDING {week_ending}:\n"
                           f"Opened week at: ${last_week_open}\n"
                           f"Closed week at: ${last_week_close}\n"
                           f"Weekly difference: {last_week_percent}%\n"
                           f"Last week's high: ${last_week_high}\n"
                           f"Last week's low: ${last_week_low}\n")


    #-----MONTHLY DATA -----#
    MONTHLY_PARAMS = {
        "function": "TIME_SERIES_MONTHLY",
        "symbol": stock_code,
        "apikey": STOCK_API_KEY
    }

    response = requests.get(STOCK_ENDPOINT, params=MONTHLY_PARAMS)
    monthly_data = response.json()["Monthly Time Series"]
    month_ending = (str(monthly_data).split(":")[6].split("'")[3])

    monthly_data_list = [value for (key, value) in monthly_data.items()]
    last_month_open = monthly_data_list[1]["1. open"]
    last_month_close = monthly_data_list[1]["4. close"]
    last_month_percent = round((float(last_month_close) - float(last_month_open)) * 100 / float(last_month_open), 2)
    last_month_high = monthly_data_list[1]["2. high"]
    last_month_low = monthly_data_list[1]["3. low"]

    monthly_data_message = (f"\nDATA FOR MONTH ENDING {month_ending}:\n"
                           f"Opened month at: ${last_month_open}\n"
                           f"Closed month at: ${last_month_close}\n"
                           f"monthly difference: {last_month_percent}%\n"
                           f"Last month's high: ${last_month_high}\n"
                           f"Last month's low: ${last_month_low}"
                            )

    #-----COMPILED MESSAGES -----#
    div = (f"Here is the information you requested for {stock_code}:\n"
           f"Name: {company_name}\n"
           f"{overview_message_div}"
           f"{weekly_data_message}\n"
           f"{monthly_data_message}\n"
          )

    no_div = (f"Here is the information you requested for {stock_code}:\n"
           f"Name: {company_name}\n"
           f"{overview_message_no_div}"
           f"{weekly_data_message}\n"
           f"{monthly_data_message}\n"
          )

    if company_div_amount == 0:
        return no_div
    else:
        return div