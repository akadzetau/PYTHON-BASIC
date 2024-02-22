from task_5 import make_request
from unittest.mock import Mock


def test_make_request():
    test_cases = {"case1": {'url': 'https://www.google.com', 'response': 200},
                  "case2": {'url': 'https://www.ffffffff.ru'}}

    for case_key, case_value in test_cases.items():
        res = make_request(case_value['url'])
        assert res is not None, "make_request should not return None"
        assert type(res) is tuple, "make_request should return a tuple"
        assert len(res) == 2, "make_request should return a tuple of 2 elements"

        resp_code = case_value.get('response', -1)
        assert (resp_code == 200) == (resp_code == res[0]), "make_request should return expected code value"
        assert (resp_code == 200) == ('HTML' in res[1].upper()), "make_request should return HTML page"


def test_make_request1():
    expectation = (200, 'something')

    m = Mock()
    m.print_name_address.return_value = expectation

    assert m.print_name_address() == expectation
