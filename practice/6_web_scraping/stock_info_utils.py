import regex
import logging
from datetime import datetime


def get_country(soup, stock):
    try:
        address = soup.find("div", {"class": "asset-profile-container"}).find("div").find("div").find_all("p")[0] \
            .find_all(string=regex.compile("^[^0-9]+$"))
        if "http" in address[-1]: address.pop()
        return address[-1]
    except Exception as e:
        logging.error(f'Getting Country for {stock} exception: {e}')


def get_employees(soup, stock):
    try:
        return int(list(soup.find("div", {"class": "asset-profile-container"}).find("div").find("div")
                        .find_all("p")[1].stripped_strings)[8].replace(",", ""))
    except Exception as e:
        logging.error(f'Getting Employees for {stock} exception: {e}')


def get_ceo_name(soup, stock):
    ceo = soup.find("div", {"id": "Main"}).find("div").find("section").find("table").find(string=regex.compile("CEO"))
    if ceo:
        try:
            return ceo.parent.parent.parent.find_all("td")[0].text
        except Exception as e:
            logging.error(f'Getting CEO name for {stock} exception: {e}')


def get_ceo_year_born(soup, stock):
    ceo = soup.find("div", {"id": "Main"}).find("div").find("section").find("table").find(string=regex.compile("CEO"))
    if ceo:
        try:
            ceo_year_born = ceo.parent.parent.parent.find_all("td")[4].text
            if ceo_year_born != 'N/A':
                return int(ceo_year_born)
        except Exception as e:
            logging.error(f'Getting CEO Year Born for {stock} exception: {e}')


def get_total_cash(soup, stock):
    sh = {"K": 1000, "M": 1000000, "B": 1000000000, "T": 1000000000000,}
    try:
        total = soup.find("h3", string="Balance Sheet").parent.find("table").find("span", string="Total Cash") \
            .parent.parent.find_all("td")[1].text
        if total != 'N/A':
            return float(total[:-1]) * sh.get(total[-1], 1)
    except Exception as e:
        logging.error(f'Getting Total cash for {stock} exception: {e}')


def get_week_change_52(soup, stock):
    try:
        week_change52 = soup.find("h3", string="Stock Price History").parent.find("table") \
            .find("span", string="52-Week Change").parent.parent.find_all("td")[1].text.replace("%", "")
        if week_change52 != 'N/A':
            return float(week_change52)
    except Exception as e:
        logging.error(f'Getting Week Change for {stock} exception: {e}')


def get_symbols_table(soup):
    return soup.find("div", {"id": "scr-res-table"}).find_all("tr", {"class": "simpTblRow"})


def get_symbol(stock):
    return stock.find("td", {"aria-label": "Symbol"}).find("a", href=True).text


def get_symbol_href(stock):
    return stock.find("td", {"aria-label": "Symbol"}).find("a", href=True)['href']


def get_symbol_name(stock):
    return stock.find("td", {"aria-label": "Name"}).text


def get_pages(soup, rx_pages):
    return soup.find("div", {"id": "fin-scr-res-table"}).find("div").find("div")\
        .find(string=regex.compile(rx_pages))


def get_holders_table(soup):
    return soup.find("span", string="Top Institutional Holders").parent.parent.find("table").find("tbody").find_all("tr")


def get_holder_name(holder, column):
    return holder.find_all("td")[column].text


def get_holder_shares(holder, column):
    return int(holder.find_all("td")[column].text.replace(",", ""))


def get_holder_date_reported(holder, column):
    return datetime.strftime(datetime.strptime(holder.find_all("td")[column].text, "%b %d, %Y"), "%Y-%m-%d")


def get_holder_p_out(holder, column):
    return float(holder.find_all("td")[column].text[:-1])


def get_holder_value(holder, column):
    return int(holder.find_all("td")[column].text.replace(",", ""))
