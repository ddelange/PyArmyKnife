import pytest

from pyarmyknife.www import extract_domain


@pytest.mark.parametrize(
    "bad_url",
    [
        "x" * 2000 + "too_long.com",
        "https://localhost:8080",
        "https://例子.测试",
        "http://223.255.255.254",
        "http:///www.github.io",
    ],
)
def test_extract_no_domain(bad_url):
    assert extract_domain(bad_url) is None, bad_url


@pytest.mark.parametrize(
    "website, domain",
    [
        ("https://www.unicode.emoji💥.ws", "unicode.emoji💥.ws"),
        ("JP納豆.例.jp", "jp納豆.例.jp"),
        ("www.gob.mx", "www.gob.mx"),
    ],
)
def test_extract_domain(website, domain):
    assert extract_domain(website) == domain
