import requests
import yfinance

# Replace 'your_api_key_here' with your actual Alpha Vantage API key
API_KEY = 'your_api_key_here'
BASE_URL = 'https://www.alphavantage.co/query'

portfolio = {}

def get_stock_price(symbol):
    """Fetch real-time stock price for a given symbol."""
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '1min',
        'apikey': API_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        # Check if data contains the required key
        if 'Time Series (1min)' not in data:
            print(f"Error: Unable to fetch data for {symbol}.")
            return None
        
        latest_time = list(data['Time Series (1min)'].keys())[0]
        price = data['Time Series (1min)'][latest_time]['1. open']
        return float(price)
    
    except (KeyError, ValueError) as e:
        print(f"Error: {e}.")
        return None

def add_stock(symbol, shares):
    """Add a stock to the portfolio."""
    price = get_stock_price(symbol)
    if price:
        portfolio[symbol] = {
            'shares': shares,
            'price': price
        }
        print(f"Added {symbol}: {shares} shares at ${price:.2f} per share.")

def remove_stock(symbol):
    """Remove a stock from the portfolio."""
    if symbol in portfolio:
        del portfolio[symbol]
        print(f"Removed {symbol} from the portfolio.")
    else:
        print(f"Error: {symbol} is not in the portfolio.")

def view_portfolio():
    """Display the portfolio and total value."""
    total_value = 0
    print("\nYour Portfolio:")
    for symbol, info in portfolio.items():
        price = get_stock_price(symbol)
        if price:
            value = info['shares'] * price
            total_value += value
            print(f"{symbol}: {info['shares']} shares at ${price:.2f} per share. Value: ${value:.2f}")
        else:
            print(f"{symbol}: Unable to fetch latest price.")
    print(f"\nTotal Portfolio Value: ${total_value:.2f}\n")

def main():
    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. View Portfolio")
        print("4. Exit")

        choice = input("Enter your choice: ")
        
        if choice == '1':
            symbol = input("Enter stock symbol: ").upper()
            shares = int(input("Enter number of shares: "))
            add_stock(symbol, shares)
        
        elif choice == '2':
            symbol = input("Enter stock symbol to remove: ").upper()
            remove_stock(symbol)
        
        elif choice == '3':
            view_portfolio()
        
        elif choice == '4':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
