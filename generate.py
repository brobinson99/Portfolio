import pandas as pd
import numpy as np

product_cats = ['a', 'b', 'c', 'd']

outlet_locations = ['Region A', 'Region B', 'Region C', 'Region D']

#generate list of dates from start date to end date by step D
def generate_dates(start_date, end_date):
    return pd.date_range(start=start_date, end=end_date, freq='D')


def generate_day(date, orders=5000, month_trend = 0.1, seasonality = 0.2, rand = None):

    month = date.month

    #sine curve fitting for seasonality data, assume dip and peak (basically)
    season = 1 + seasonality * np.sin(2 * np.pi * month / 12)

    #track months passed since start of data generation
    months_passed = (date.year - 2000) * 12 + date.month

    #assigning trend in data
    data_trend = 1 + month_trend * (months_passed % 120)

    #simulating orders , why poisson????
    L = orders * season * data_trend
    actual_orders = max(0, rand.poisson(L))

    rows = []
    for i in range(orders):

        #need to simulate order id, customer id, and prices per category
        #order id will be unique per column, primary key
        #order id also needs to take into account date order was ordered
        order_id = f"{date.strftime('%Y%m%d')}_{i}"

        #customer id for now is just a number
        customer_id = rand.integers(1,999)

        #assigning weights to each category, will be able to randomly generate eventually
        category = rand.choice(product_cats, p=[0.5, 0.3, 0.1, 0.1])
        location = rand.choice(outlet_locations, p=[0.6, 0.2, 0.15, 0.05])

        #time to simulate prices, im going to choose random base prices
        base_prices = {
            'a':rand.uniform(10, 100),
            'b':rand.uniform(5,100),
            'c':rand.uniform(5, 50),
            'd':rand.uniform(1, 30)
        }[category]

        #HERE is where any discount or promotion columns would go. leaving for now

        #time to calculate the sales metrics
        price = round(base_prices, 2)
        quantity = int(max(1, rand.poisson(2)))
        value = round(price * quantity, 2)

        #inserting rows!
        rows.append([date.date(), order_id, customer_id, category, location, price, quantity, value])
    return rows

def main():

    rand = np.random.default_rng(67)
    dates = generate_dates("2023/01/01", "2025/12/31")

    all_rows = []
    for date in dates:
        all_rows.extend(generate_day(date, rand=rand))

    df = pd.DataFrame(
        all_rows,
        columns=['date', 'order_id', 'customer_id', 'category', 'location', 'price', 'quantity', 'value']
    )
    df['date'] = pd.to_datetime(df['date'])
    df.to_csv('data/sales_data_v2.csv', index=False)

if __name__ == "__main__":
    main()