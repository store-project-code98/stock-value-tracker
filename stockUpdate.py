db = mysql.connector.connect(
    host="localhost",         
    user="root",   
    password="",  
)
cursor = db.cursor()

API_KEY = ''

symbol = 'AAPL'
url = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}'

response = requests.get(url)
data = response.json()

print(json.dumps(data, indent=4))

cursor.execute("CREATE DATABASE IF NOT EXISTS stock_data_db")

cursor.execute("USE stock_data_db")

cursor.execute('''
CREATE TABLE IF NOT EXISTS stock_data (
    symbol VARCHAR(10) PRIMARY KEY, 
    name VARCHAR(255),
    current_price FLOAT,
    high FLOAT,
    low FLOAT,
    open FLOAT,
    previous_close FLOAT
)
''')

link = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks"

df = pd.read_html(link, header=0)[0]

top_500_symbols = df['Symbol'].tolist()
top_500_names = df['Security'].tolist()

def fetch_stock_data(symbol):
    url = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()  
    else:
        print(f"Error fetching data for {symbol}: {response.status_code}")
        return None

rateLimit = 0

for i in range(len(top_500_symbols)):
    data = fetch_stock_data(top_500_symbols[i])
    rateLimit += 1
    if rateLimit > 20:
        rateLimit = 0
        time.sleep(30)
    
    if data and None not in (data['c'], data['h'], data['l'], data['o'], data['pc']):
        cursor.execute('''
        INSERT INTO stock_data (symbol, name, current_price, high, low, open, previous_close)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            current_price = VALUES(current_price),
            high = VALUES(high),
            low = VALUES(low),
            open = VALUES(open),
            previous_close = VALUES(previous_close)
        ''', (
            top_500_symbols[i], 
            top_500_names[i],
            data['c'],  
            data['h'],  
            data['l'],  
            data['o'],  
            data['pc']  
        ))
    else:
        print(f"Invalid data for {top_500_symbols[i]}, skipping insert.")

    print(top_500_symbols[i])

    db.commit()

db.close()

print(f"Stock data for top 500 symbols has been stored in the MySQL database.")

