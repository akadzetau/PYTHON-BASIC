from stock_info_utils import get_country, get_employees, get_ceo_name, \
    get_ceo_year_born, get_total_cash, get_week_change_52, get_symbol_href, get_symbol_name, \
    get_holder_name, get_holder_shares, get_holder_date_reported, get_holder_p_out, get_holder_value

base_url = "https://finance.yahoo.com"
user_agent = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
    'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',
    'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
    'Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0',
]
steps_config = {"MostActive": {"file": "most_active.json",
                               "url_template": base_url + "/most-active",
                               "params": {"href": get_symbol_href,
                                          "name": get_symbol_name
                                         }
                               },
                "Profile": {"file": "most_active_profile.json",
                            "url_template": base_url + "/quote/{stock}/profile",
                            "params": {"country": get_country,
                                       "employees": get_employees,
                                       "CEOName": get_ceo_name,
                                       "CEOYearBorn": get_ceo_year_born},
                            },
                "Statistics": {"file": "most_active_statistics.json",
                               "url_template": base_url + "/quote/{stock}/key-statistics",
                               "params": {"totalCash": get_total_cash,
                                          "weekChange52": get_week_change_52},
                               },
                "BLKHolders": {"file": "blk_holders.json",
                               "url_template": base_url + "/quote/BLK/holders",
                               "params": {"holder": get_holder_name,
                                          "shares": get_holder_shares,
                                          "dateReported": get_holder_date_reported,
                                          "pOut": get_holder_p_out,
                                          "value": get_holder_value,
                                          }
                               },
                }
