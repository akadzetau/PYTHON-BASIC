from task_1 import calculate_days, WrongFormatException
import pytest


@pytest.mark.freeze_time('2021-10-06')
def test_calculate_days_past():
    result = calculate_days('2021-10-05')
    assert result == 1


@pytest.mark.freeze_time('2021-10-06')
def test_calculate_days_future():
    result = calculate_days('2021-10-07')
    assert result == -1


def test_calculate_days_wrong_format():
    with pytest.raises(WrongFormatException, match="Wrong date format"):
        result = calculate_days('10-07-2021')
        assert result is None
