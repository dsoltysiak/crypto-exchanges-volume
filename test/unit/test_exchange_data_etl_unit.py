import datetime

from cryptomonitor.exchange_data_etl import get_utc_from_unix_time


def test_get_utc_from_unix_time():
    ut: int = 1645444380183
    expected_dt = datetime.datetime(2022, 2, 21, 11, 53, 00, 183000)
    assert expected_dt == get_utc_from_unix_time(ut)
