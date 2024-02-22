import io
import unittest
from unittest.mock import patch
from stock_info import get_soup, print_sheet
from bs4 import BeautifulSoup


class MyTestCase(unittest.TestCase):
    @patch('stock_info.requests.get')
    def test_request_soup_ok(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = "<html/>"
        res = get_soup("http://test_url", {})
        assert isinstance(res, BeautifulSoup)

    @patch('stock_info.requests.get')
    def test_request_soup_fail(self, mock_get):
        mock_get.return_value.status_code = 201
        with self.assertRaises(Exception) as context:
            get_soup("http://test_url", {})
        self.assertEqual(str(context.exception), f"Requests exception: Status code {201}")

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_print_sheet(self, mock_stdout):
        expected = """==================================== 5 stocks with most youngest CEOs ===================================
| Name        | Code | Country       | Employees | CEO Name                             | CEO Year Born |
---------------------------------------------------------------------------------------------------------
| Pfizer Inc. | PFE  | United States | 78500     | Dr. Albert Bourla D.V.M., DVM, Ph.D. | 1962          |

"""
        print_sheet([["Pfizer Inc.", "PFE", "United States", 78500, "Dr. Albert Bourla D.V.M., DVM, Ph.D.", 1962]],
                    ["Name", "Code", "Country", "Employees", "CEO Name", "CEO Year Born"],
                    "5 stocks with most youngest CEOs")
        self.assertEqual(mock_stdout.getvalue(), expected)