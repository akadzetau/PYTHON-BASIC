from task_4 import print_name_address
import argparse
from unittest.mock import patch, Mock
import io


@patch('sys.stdout', new_callable=io.StringIO)
def test_print_name_address(mock_stdout):
    test_cases = {"case1": {'NUMBER': 2, '--fake-address': 'address', '--some_name': 'name'},
                  "case2": {'NUMBER': 3, '--fake_company': 'company', '--fake-color': 'color'}}
    args = argparse.Namespace

    for case in test_cases:
        keys = []
        for attr_k, attr_v in test_cases[case].items():
            setattr(args, attr_k, attr_v)
            if attr_k.startswith("--"):
                keys.append(attr_k.replace("--", ""))
        n_lines = test_cases[case]['NUMBER']

        assert print_name_address(args) is None, "print_name_address should return None"

        printed_lines = mock_stdout.getvalue().split("\n")[-n_lines-1::] # Get latest N+1 printed lines
        assert len(printed_lines) == n_lines + 1, f"{n_lines} lines should be printed"
        for line in range(n_lines):
            line_dict = eval(printed_lines[line])
            assert type(line_dict) is dict, "print_name_address should print Dictionaries"
            assert sorted(line_dict.keys()) == sorted(keys), f"print_name_address keys should contais {keys}"

        # Clean args
        for el in test_cases[case]:
            delattr(args, el)


def test_print_name_address1():
    expectation = {'fake-address': 'address', 'some_name': 'name'}

    m = Mock()
    m.print_name_address.return_value = expectation

    assert m.print_name_address() == expectation
