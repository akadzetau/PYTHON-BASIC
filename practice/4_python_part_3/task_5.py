"""
Write a function that makes a request to some url
using urllib. Return status code and decoded response data in utf-8
Examples:
     >>> make_request('https://www.google.com')
     200, 'response data'
"""
from typing import Tuple
from urllib import request, error

def make_request(url: str) -> Tuple[int, str]:
    try:
        resp = request.urlopen(url)
        return (resp.code, resp.read().decode(resp.headers.get_content_charset()).encode('utf-8').decode('utf-8'))
    except error.HTTPError as e:
        return (e.reason.errno, e.reason.strerror)
    except error.URLError as e:
        return (e.reason.errno, e.reason.strerror)


"""
Write test for make_request function
Use Mock for mocking request with urlopen https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 200
    >>> m.method2.return_value = b'some text'
    >>> m.method()
    200
    >>> m.method2()
    b'some text'
"""
