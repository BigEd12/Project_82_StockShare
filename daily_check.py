import requests
import stocker
from stocks import stocks

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "GBT0OSG8WZ453JN"
NEWS_API_KEY = "e4e110670cc04cc584fa1f30ef9d35b8"

def daily_check(stock_code, percentage_diff):


    STOCK_PARAMETERS = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": stock_code,
        "apikey": STOCK_API_KEY
    }

    response = requests.get(STOCK_ENDPOINT, params=STOCK_PARAMETERS)
    stock_data = response.json()
    stock_data_daily = stock_data["Time Series (Daily)"]

    #---------- STOCK VARIANCE ----------#
    #----- FIND PRICES -----#
    data_list = [value for (key, value) in stock_data_daily.items()]
    stock_yday_open = float(data_list[0]["1. open"])
    stock_yday_close = float(data_list[0]["4. close"])
    difference = abs(stock_yday_open - stock_yday_close)
    percentage_difference = round(difference / stock_yday_close * 100, 2)

    if percentage_difference >= float(percentage_diff):
        NEWS_PARAMETERS = {
            "apiKey": NEWS_API_KEY,
            "q": stock_code,
            "sortBy": "publishedAt"
        }
        # ----- FIND ARTICLES -----#
        news_response = requests.get(url=NEWS_ENDPOINT, params=NEWS_PARAMETERS)
        news_data = news_response.json()["articles"]
        top_3 = news_data[:3]

        title_1 = top_3[0]["title"]
        description_1 = top_3[0]["description"]
        url_1 = top_3[0]["url"]
        title_2 = top_3[1]["title"]
        description_2 = top_3[1]["description"]
        url_2 = top_3[1]["url"]
        title_3 = top_3[2]["title"]
        description_3 = top_3[2]["description"]
        url_3 = top_3[2]["url"]
        news_list = [(title_1, description_1, url_1), (title_2, description_2, url_2), (title_3, description_3, url_3)]


        def difference_direction():
            if stock_yday_close < stock_yday_open:
                return "📉"
            elif stock_yday_close > stock_yday_open:
                return "📈"


        # ----- SEND ARTICLES -----#
        message = f"Subject Swing in {stock_code} Price {difference_direction()}\n\n" \
                  f"Hey Eddie\n\n" \
                  f"There has been a swing of {percentage_difference}% in {stock_code}.\n\n" \
                  f"Here are the top three stories found:\n\n" \
                  f"Headline: {news_list[0][0]}\n" \
                  f"Brief: {news_list[0][1]}\n" \
                  f"Link to Story:{news_list[0][2]}\n\n" \
                  f"Headline: {news_list[1][0]}\n" \
                  f"Brief: {news_list[1][1]}\n" \
                  f"Link to Story:{news_list[1][2]}\n\n" \
                  f"Headline: {news_list[2][0]}\n" \
                  f"Brief: {news_list[2][1]}\n" \
                  f"Link to Story:{news_list[2][2]}"

        encoded_message = message.encode("utf-8")

        return message
    else:
        return f"The price difference yesterday was: {percentage_difference}%, less than the threshold of {percentage_diff}% you set to receive news stories."

def predictor(stock_code):
    STOCK_PARAMETERS = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": stock_code,
        "apikey": STOCK_API_KEY
    }

    response = requests.get(STOCK_ENDPOINT, params=STOCK_PARAMETERS)
    stock_data = response.json()
    stock_data_daily = stock_data["Time Series (Daily)"]

    # ----- FIND PRICES -----#
    data_list = [value for (key, value) in stock_data_daily.items()]
    stock_yday_open = float(data_list[0]["1. open"])
    stock_yday_close = float(data_list[0]["4. close"])
    difference = stock_yday_close - stock_yday_open
    percentage_difference_yday = round(difference / stock_yday_close * 100, 2)

    predicted_price, error, date = stocker.predict.tomorrow(stock_code)

    predicted_difference = predicted_price - stock_yday_close
    percentage_difference_tmrw = round(predicted_difference / predicted_price * 100, 2)

    message = f"You requested information for {stock_code}:\n\n" \
              f"Last available price information for {stock_code}:\n\n" \
              f"Opened at: ${stock_yday_open}\n" \
              f"Closed at: ${stock_yday_close}\n" \
              f"Swing was: {percentage_difference_yday}%\n\n" \
              f"{date} predicted close: ${predicted_price}\n" \
              f"Predicted difference: {percentage_difference_tmrw}%\n"

    return message

def predict_all(user_difference):
    all_alerts = []
    for stock_code in stocks:
        STOCK_PARAMETERS = {
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": stock_code,
            "apikey": STOCK_API_KEY
        }

        response = requests.get(STOCK_ENDPOINT, params=STOCK_PARAMETERS)
        stock_data = response.json()
        stock_data_daily = stock_data["Time Series (Daily)"]

        # ----- FIND PRICES -----#
        data_list = [value for (key, value) in stock_data_daily.items()]
        stock_yday_open = float(data_list[0]["1. open"])
        stock_yday_close = float(data_list[0]["4. close"])
        difference = stock_yday_close - stock_yday_open
        percentage_difference_yday = round(difference / stock_yday_close * 100, 2)

        predicted_price, error, date = stocker.predict.tomorrow(stock_code)

        predicted_difference = predicted_price - stock_yday_close
        percentage_difference_tmrw = round(predicted_difference / predicted_price * 100, 2)

        if percentage_difference_tmrw > user_difference or percentage_difference_tmrw < - user_difference:
            message = f"You requested information for {stock_code}:\n\n" \
                      f"Last available price information for {stock_code}:\n\n" \
                      f"Opened at: ${stock_yday_open}\n" \
                      f"Closed at: ${stock_yday_close}\n" \
                      f"Swing was: {percentage_difference_yday}%\n\n" \
                      f"{date} predicted close: ${predicted_price}\n" \
                      f"Predicted difference: {percentage_difference_tmrw}%\n"
            all_alerts.append(message)
        else:
            return f"No stocks will change by more than {user_difference}%"
    return all_alerts