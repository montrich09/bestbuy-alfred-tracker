import os
import requests
import os.path
from datetime import date
from datetime import timedelta
import pandas as pd
import matplotlib.pyplot as plt

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If python-dotenv is not installed, continue without it
    pass


def get_product(link):
    # Get credentials from environment variables
    USERNAME = os.getenv('OXYLABS_USERNAME')
    PASSWORD = os.getenv('OXYLABS_PASSWORD')
    
    # Check if credentials are available
    if not USERNAME or not PASSWORD:
        raise ValueError("OXYLABS_USERNAME and OXYLABS_PASSWORD environment variables must be set")

    # Structure payload.
    payload = {
        'source': 'universal_ecommerce',
        'url': link,
        'geo_location': 'United States',
        'parse': True,
    }

    # Get response.
    response = requests.request(
        'POST',
        'https://realtime.oxylabs.io/v1/queries',
        auth=(USERNAME, PASSWORD),
        json=payload,
    )
    response_json = response.json()

    # # Debug: Print the response structure
    # print("Response status code:", response.status_code)
    # print("Response keys:", list(response_json.keys()) if isinstance(response_json, dict) else "Not a dict")
    
    content = response_json["results"][0]["content"]
    
    # Debug: Print content structure
    print("Content keys:", list(content.keys()) if isinstance(content, dict) else "Not a dict")
    if 'price' in content:
        print("Price structure:", content['price'])

    # Handle price parsing with error checking
    price_value = "Price not available"
    currency_value = "Currency not available"
    
    if isinstance(content["price"], dict):
        if "price" in content["price"]:
            price_data = content["price"]["price"]
            if isinstance(price_data, (int, float)) or (isinstance(price_data, str) and not price_data.startswith("Error")):
                price_value = price_data
            else:
                print(f"Price parsing error: {price_data}")
        
        if "currency" in content["price"]:
            currency_data = content["price"]["currency"]
            if isinstance(currency_data, str) and not currency_data.startswith("Error"):
                currency_value = currency_data
            else:
                print(f"Currency parsing error: {currency_data}")

    product = {
        "title": content["title"],
        "price": price_value,
        "currency": currency_value
    }
    return product

def read_past_data(filepath):
    results = {}

    if not os.path.isfile(filepath):
        open(filepath, 'a').close()

    if not os.stat(filepath).st_size == 0:
        results_df = pd.read_json(filepath, convert_axes=False)
        results = results_df.to_dict()
        return results
    
    return results

def save_results(results, filepath):
    df = pd.DataFrame.from_dict(results)

    df.to_json(filepath)

    return

def add_todays_prices(results, tracked_product_links):
    today = date.today()

    for link in tracked_product_links:
        product = get_product(link)

        if product["title"] not in results:
            results[product["title"]] = {}
        
        results[product["title"]][today.strftime("%d %B, %Y")] = {
            "price": product["price"],
            "currency": product["currency"],
        }
    
    return results

def plot_history_chart(results):
    for product in results:
        dates = []
        prices = []
        
        for entry_date in results[product]:
            dates.append(entry_date)
            prices.append(results[product][entry_date]["price"])

        plt.plot(dates,prices, label=product)
        
        plt.xlabel("Date")
        plt.ylabel("Price")

    plt.title("Product prices over time")
    plt.legend()
    plt.show()

def check_for_pricedrop(results):
    for product in results:
        today = date.today()
        yesterday = today - timedelta(days = 1)
        
        today_str = today.strftime("%d %B, %Y")
        yesterday_str = yesterday.strftime("%d %B, %Y")
        
        # Check if we have data for both today and yesterday
        if today_str in results[product] and yesterday_str in results[product]:
            change = results[product][today_str]["price"] - results[product][yesterday_str]["price"]

            if change < 0:
                print(f'Price for {product} has dropped by {change}!')
        else:
            print(f'Not enough data to check price drop for {product} (need both today and yesterday)')


def main():
    results_file = "data.json"

    tracked_product_links = [
        "https://www.bestbuy.com/site/samsung-galaxy-z-flip4-128gb-unlocked-graphite/6512618.p?skuId=6512618&intl=nosplash",
        "https://www.bestbuy.com/site/samsung-galaxy-z-flip5-256gb-unlocked-graphite/6548838.p?skuId=6548838"
    ]

    past_results = read_past_data(results_file)

    updated_results = add_todays_prices(past_results, tracked_product_links)

    # plot_history_chart(updated_results)

    # check_for_pricedrop(updated_results)

    save_results(updated_results, results_file)
    
if __name__ == "__main__":
    main()