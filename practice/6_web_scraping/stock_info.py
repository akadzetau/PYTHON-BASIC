"""
There is a list of most active Stocks on Yahoo Finance https://finance.yahoo.com/most-active.
You need to compose several sheets based on data about companies from this list.
To fetch data from webpage you can use requests lib. To parse html you can use beautiful soup lib or lxml.
Sheets which are needed:
1. 5 stocks with most youngest CEOs and print sheet to output. You can find CEO info in Profile tab of concrete stock.
    Sheet's fields: Name, Code, Country, Employees, CEO Name, CEO Year Born.
2. 10 stocks with best 52-Week Change. 52-Week Change placed on Statistics tab.
    Sheet's fields: Name, Code, 52-Week Change, Total Cash
3. 10 largest holds of Blackrock Inc. You can find related info on the Holders tab.
    Blackrock Inc is an investment management corporation.
    Sheet's fields: Name, Code, Shares, Date Reported, % Out, Value.
    All fields except first two should be taken from Holders tab.


Example for the first sheet (you need to use same sheet format):
==================================== 5 stocks with most youngest CEOs ===================================
| Name        | Code | Country       | Employees | CEO Name                             | CEO Year Born |
---------------------------------------------------------------------------------------------------------
| Pfizer Inc. | PFE  | United States | 78500     | Dr. Albert Bourla D.V.M., DVM, Ph.D. | 1962          |
...

About sheet format:
- sheet title should be aligned to center
- all columns should be aligned to the left
- empty line after sheet

Write at least 2 tests on your choose.
Links:
    - requests docs: https://docs.python-requests.org/en/latest/
    - beautiful soup docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    - lxml docs: https://lxml.de/
"""
import time
import requests
from bs4 import BeautifulSoup
import regex
import json
import os
import random
import logging
from stock_info_config import steps_config, user_agent
from stock_info_utils import get_symbols_table, get_symbol, get_pages
from stock_info_utils import get_holders_table


def get_soup(url, params):
    time.sleep(5)
    req = requests.get(url, params=params, headers={'User-Agent': random.choice(user_agent)}, timeout=5)
    if req.status_code == 200:
        return BeautifulSoup(req.content, "html.parser")
    else:
        raise Exception(f"Requests exception: Status code {req.status_code}")


def write_step(file_name, stocks):
    js = json.dumps(stocks, indent=4)
    with open(file_name, 'w') as f:
        f.write(js)


def read_step(file_name, step):
    if os.path.isfile(file_name):
        with open(file_name, 'r') as f:
            stocks = json.loads(f.read())
            logging.info(f"{len(stocks)} Stocks on step {step} are loaded from cache")
            return stocks
    else:
        return {}


def get_stocks():
    # Step 1: ============ Get list of Most active Stocks ============
    logging.info("Getting Most active stocks")
    step = "MostActive"

    # Load Most Active from cache
    stocks = read_step(steps_config[step]["file"], step)
    if not stocks:
        rx_pages = r"^(\d+)-(\d+) of (\d+) results"
        has_next = True
        stocks_on_page = 25
        offset = 0
        while has_next:
            try:
                soup = get_soup(steps_config[step]["url_template"],
                                params={"count": stocks_on_page, "offset": offset})
                for stock in get_symbols_table(soup):
                    symbol = get_symbol(stock)
                    stocks[symbol] = {}
                    for param in steps_config[step]["params"]:
                        param_value = steps_config[step]["params"][param](stock)
                        if param_value:
                            stocks[symbol][param] = param_value

                pages = get_pages(soup, rx_pages)
                offset = int(regex.match(rx_pages, pages).group(2))
                total = int(regex.match(rx_pages, pages).group(3))
                has_next = offset < total
                logging.info(f"Pages: {pages}, Has next page: {has_next}, Offset: {offset}")
            except:
                logging.error(f"Getting stock list failed offset: {offset}")
                raise Exception("Not all pages are loaded")
        logging.info(f"Total most active stocks scrapped: {len(stocks)}")
        write_step(steps_config[step]["file"], stocks)

    # Step 2,3: ============ Getting stock's profiles and statistics ============
    for step in ["Profile", "Statistics"]:
        logging.info(f"Getting stocks {step}")

        # Load Stock's profiles/statistics from cache
        stocks_ch = read_step(steps_config[step]["file"], step)
        if stocks_ch:
            for stock in stocks:
                for param in steps_config[step]["params"]:
                    if stocks_ch[stock].get(param, None):
                        stocks[stock][param] = stocks_ch[stock][param]

        logging.info(f"Getting {step} values")
        for stock in stocks:
            url = steps_config[step]["url_template"].format(stock=stock)
            req_params = {"p": stock}
            soup = None
            # Do the request only if One of params is empty then
            try:
                for param in steps_config[step]["params"]:
                    if stocks[stock].get(param, None) is None:
                        soup = get_soup(url, params=req_params)
                        break
            except Exception as e:
                logging.warning(f"Getting {stock}'s {step} failed: {e}")

            if soup:
                for param in steps_config[step]["params"]:
                    param_value = steps_config[step]["params"][param](soup, stock)
                    if param_value:
                        stocks[stock][param] = param_value

        write_step(steps_config[step]["file"], stocks)
        logging.info(f"Done with Getting stocks {step}")

    return stocks


def get_blk_holders():
    logging.info("Getting BLK Holders")
    step = "BLKHolders"

    # Load Most Active from cache
    holders = read_step(steps_config[step]["file"], step)
    if not holders:
        try:
            soup = get_soup(steps_config[step]["url_template"], params={"p": "BLK"})
            holders["BLK"] = {}
            holders["BLK"]["name"] = "Blackrock Inc"
            holders["BLK"]["params"] = []
            for holder in get_holders_table(soup):
                h = {}
                for i, param in enumerate(steps_config[step]["params"]):
                    param_value = steps_config[step]["params"][param](holder, i)
                    if param_value:
                        h[param] = param_value
                holders["BLK"]["params"].append(h)
        except:
            logging.error(f"Getting BLK Holders list failed")
            raise Exception("Getting BLK Holders list failed")
        logging.info(f"BLK Holders are scrapped: {len(holders['BLK'])}")
        write_step(steps_config[step]["file"], holders)

    return holders


def get_stocks_by_ceo_age(stocks):
    stocks_by_ceo_age = [[v.get("name", None), k, v.get("country", None), v.get("employees", None),
                          v.get("CEOName", None), v.get("CEOYearBorn", 0)] for k, v in stocks.items()]
    return sorted(stocks_by_ceo_age, key=lambda x:x[5], reverse=True)[:5]


def get_stocks_by_52_week_change(stocks):
    stocks_by_52_week_change = [[v.get("name", None), k, v.get("weekChange52", None), v.get("totalCash", None)]
                                for k, v in stocks.items()]
    return sorted(stocks_by_52_week_change, key=lambda x:x[2], reverse=True)[:10]


def get_holders(holders):
    code = list(holders.keys())[0]
    h = [[k.get("holder", None), k.get("shares", None), k.get("dateReported", None), k.get("pOut", None),
          k.get("value", None)] for k in holders[code]["params"]]
    return sorted(h, key=lambda x:x[1], reverse=True)[:10]


def print_sheet(values, header, title):
    lengths = {}
    for entry in values + [header]:
        for n, el in enumerate(entry):
            if len(str(el)) > lengths.get(n, 0):
                lengths[n] = len(str(el))

    # Sum of LengthOfEachElement + NumberOfElements * (2 alignments + separator) + 1 left separator
    sheet_length = sum(lengths.values()) + len(lengths) * 3 + 1
    print(f" {title} ".center(sheet_length, "="))
    print("|" + "|".join([f" {h.ljust(lengths[i])} " for i, h in enumerate(header)]) + "|")
    print("".center(sheet_length, "-"))
    for entry in values:
        print("|" + "|".join([f" {str(e).ljust(lengths[i])} " for i, e in enumerate(entry)]) + "|")
    print()


def main():
    logging.basicConfig(filename='stock_info.log', format='%(asctime)s %(levelname)s:%(message)s',
                        encoding='utf-8', level=logging.INFO)
    logging.info("------------------- New run -------------------")

    stocks = get_stocks()
    print_sheet(get_stocks_by_ceo_age(stocks),
                ["Name", "Code", "Country", "Employees", "CEO Name", "CEO Year Born"],
                "5 stocks with most youngest CEOs")

    print_sheet(get_stocks_by_52_week_change(stocks),
                ["Name", "Code", "52-Week Change", "Total Cash"],
                "10 stocks with best 52-Week Change")

    holders = get_blk_holders()
    print_sheet(get_holders(holders),
                ["Name", "Shares", "Date Reported", "% Out", "Value."],
                "10 largest holds of Blackrock Inc.")

    logging.info("----------------- We are Done -----------------")


if __name__ == "__main__":
    main()
