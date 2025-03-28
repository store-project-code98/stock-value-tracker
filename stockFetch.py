import requests
import mysql.connector
import json
import time
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

def get_stock_info(symbol):
    db = mysql.connector.connect(
        host="localhost",         
        user="root",   
        password="",  
    )
    cursor = db.cursor()

    cursor.execute("USE stock_data_db")
    cursor.execute("SELECT current_price, symbol, name, high, low, open, previous_close FROM stock_data WHERE symbol = %s", (symbol,))
    stock = cursor.fetchone()

    cursor.close()
    db.close()

    if stock:
        return {
            'price': stock[0],
            'name': stock[1],
            'symbol': stock[2],
            'high': stock[3],
            'low': stock[4],
            'open': stock[5],
            'close': stock[6],
        }
    else:
        return None

@app.route('/')
def search():
    symbol = request.args.get('s')

    if symbol:
        print(f"Search query: {symbol}")

        stock_info = get_stock_info(symbol)

        if stock_info:
            return render_template('index.html', stock_info=stock_info)
        else:
            return render_template('index.html', message="Stock symbol not found.")

    return render_template('index.html', message="Please enter a stock symbol.")

if __name__ == '__main__':
    app.run(debug=True)
