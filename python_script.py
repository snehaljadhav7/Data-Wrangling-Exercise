import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen


def daily_data():
    path = 'https://www.eia.gov/dnav/ng/hist/rngwhhdD.htm'
    page = urlopen(path)
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find(text="Week Of").find_parent("table")
    table_rows = table.find_all('tr')
    price_dict = {}
    for row in table_rows[1:]:
        td = row.find_all('td', attrs={'class': 'B6'})
        keys = [i.text.strip() for i in td]
        td = row.find_all('td', attrs={'class': 'B3'})
        values = [i.text.strip() for i in td]
        if keys:
            keys = str(keys).lstrip("['").rstrip("']")
            start_dt = keys[9:11].replace(" ", "0") + "-" + keys[5:8] + "-" + keys[0:4]
            end_dt = keys[19:22].replace(" ", "0") + "-" + keys[15:18] + "-" + keys[0:4]
            date = [d.strftime('%Y-%m-%d') for d in pd.date_range(start_dt, end_dt)]
            price_dict[tuple(date)] = values
    price_list = []
    for k in price_dict:
        for item in zip(k, price_dict[k]):
            price_list.append(item)
    df = pd.DataFrame(price_list, columns=['Date', 'Price'])
    df.to_csv('natural_gas_prices_daily.csv', index=False)


daily_data()


def monthly_data():
    path = 'https://www.eia.gov/dnav/ng/hist/rngwhhdm.htm'
    price_list = []
    month_list = []
    page = urlopen(path)
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find(text="Jan").find_parent("table")
    for p in table.find_all('td'):
        if not p.getText():
            p.replace_with("-")
    headers = table.find_all('th', attrs={'class': 'G'})

    for header in headers:
        month_list.append(header.getText().strip())
    new_row = table.find_all('tr')
    price_dict = {}
    for row in new_row[1:]:
        price_row = row.get_text().lstrip()
        if len(price_row) > 2:
            price_dict[price_row[0:4]] = price_row[5:].split()
    for key in price_dict:
        for i, price in enumerate(price_dict[key]):
            date = "1-" + month_list[i] + "-" + key
            price_list.append((date, price))
    df = pd.DataFrame(price_list, columns=['Date', 'Price'])

    df.to_csv('natural_gas_prices_monthly.csv', index=False)


monthly_data()
