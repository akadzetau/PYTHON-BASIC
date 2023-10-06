from task_2 import math_calculate, OperationNotFoundException
import pytest


def test_math_calculate_log():
    result = math_calculate('log', 1024, 2)
    assert result == 10.0


def test_math_calculate_ceil():
    result = math_calculate('ceil', 10.7)
    assert result == 11


def test_math_calculate_wrong_function():
    with pytest.raises(OperationNotFoundException) as ex:
        result = math_calculate('xxx')
        assert result is None
        assert "OperationNotFoundException: module 'math' has no attribute" in ex
