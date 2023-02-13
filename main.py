import requests
from stocks import stocks
import smtplib
import datetime
from report import initial_report
from fortnight import fortnight_report
from daily_check import daily_check, predictor, predict_all




user_choice = input("Welcome to StockShare\n\n"
                "I can offer you:\n"
                "1. An informative Report\n"
                "2. Daily Volatility Check\n"
                "3. Mid-Monthly Report\n"
                "4. Price Prediction\n"
                "Type '1', '2', '3', or '4': "
                )


if user_choice == "1":
    stock_code = input("Type in the company stock code:")
    print(initial_report(stock_code))
elif user_choice == "2":
    stock_code = input("Please input the company stock code: ")
    percentage_diff = input("At what percentage change would you like to be informed? eg: 3.3: ")
    print(daily_check(stock_code, percentage_diff))
elif user_choice == "3":
    stock_code = input("Please input the company stock code: ")
    percentage_diff = input("At what percentage change would you like to be informed? eg: 3.3: ")
    print(fortnight_report(stock_code))
elif user_choice == "4":
    indiv_group = input("Do you want to check the shares on record (1), or an individual share (2)?\nType '1' or '2': ")
    if indiv_group == "1":
        user_diff = float(input("This program will check the price at the last close of trading and compare it using Stocker against a predicted price.\n\nIf difference reaches a threshold, you will be returned a message.\n\nAt what difference would you like to be notified?: "))
        print(predict_all(user_diff))
    stock_code = input("Please input the company stock code: ").upper()
    print(predictor(stock_code))
