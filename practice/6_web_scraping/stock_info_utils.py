import regex
import logging
from datetime import datetime

sh = {"K": 1000, "M": 1000000, "B": 1000000000, "T": 1000000000000,}


def get_country(soup, stock):
    try:
        address = [l.text for l in soup.find("div", {"class": "company-info"}).find("div", {"class": "address"}).find_all("div")]
        if "http" in address[-1]: address.pop()
        return address[-1]
    except Exception as e:
        logging.error(f'Getting Country for {stock} exception: {e}')


def get_employees(soup, stock):
    try:
        return int(soup.find("div", {"class": "company-details"}).find("dl", {"class": "company-stats"})
                   .find(string=regex.compile("Full Time Employees")).parent.parent.find("dd").text.replace(',', ''))
    except Exception as e:
        logging.error(f'Getting Employees for {stock} exception: {e}')


def get_ceo_name(soup, stock):
    ceo = soup.find("main").find("section", {"data-testid": "key-executives"}).find("div", {"class": "table-container"}).find("table").find(string=regex.compile("CEO"))
    if ceo:
        try:
            return ceo.parent.parent.parent.find_all("td")[0].text
        except Exception as e:
            logging.error(f'Getting CEO name for {stock} exception: {e}')


def get_ceo_year_born(soup, stock):
    ceo = soup.find("main").find("section", {"data-testid": "key-executives"}).find("div", {"class": "table-container"}).find("table").find(string=regex.compile("CEO"))
    if ceo:
        try:
            ceo_year_born = ceo.parent.parent.parent.find_all("td")[4].text
            if ceo_year_born != 'N/A':
                return int(ceo_year_born)
        except Exception as e:
            logging.error(f'Getting CEO Year Born for {stock} exception: {e}')


def get_total_cash(soup, stock):
    try:
        total = soup.find("h3", string="Balance Sheet").parent.parent.parent.find("table").find("td", string=regex.compile("Total Cash")).parent.find_all("td")[1].text
        if total != 'N/A':
            return float(total[:-1]) * sh.get(total[-1], 1)
    except Exception as e:
        logging.error(f'Getting Total cash for {stock} exception: {e}')


def get_week_change_52(soup, stock):
    try:
        tbl = soup.find("h3", string="Stock Price History").parent.parent.parent.find("table").find_all("td")
        tbl_txt = [el.text.strip() for el in tbl]
        el = [el for el in tbl_txt if el.startswith("52 Week Range")]
        week_change52 = tbl[tbl_txt.index(el[0])+1].text.replace("%", "")
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
    return soup.find(string="Top Institutional Holders").parent.parent.parent.find("table").find("tbody").find_all("tr")


def get_holder_name(holder, column):
    return holder.find_all("td")[column].text


def get_holder_shares(holder, column):
    shares = holder.find_all("td")[column].text.replace(",", "").strip()
    return float(shares[:-1]) * sh.get(shares[-1], 1)


def get_holder_date_reported(holder, column):
    return datetime.strftime(datetime.strptime(holder.find_all("td")[column].text.strip(), "%b %d, %Y"), "%Y-%m-%d")


def get_holder_p_out(holder, column):
    return float(holder.find_all("td")[column].text.strip()[:-1])


def get_holder_value(holder, column):
    return int(holder.find_all("td")[column].text.replace(",", ""))
