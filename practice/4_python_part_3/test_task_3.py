from task_3 import is_http_domain


def test_is_http_domain_http():
    assert is_http_domain('http://wikipedia.org')


def test_is_http_domain_https():
    assert is_http_domain('https://ru.wikipedia.org/')


def test_is_http_domain_not_match():
    assert not is_http_domain('griddynamics.com')

