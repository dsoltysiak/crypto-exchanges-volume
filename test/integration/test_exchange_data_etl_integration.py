import csv
import datetime
from decimal import Decimal

import psycopg2

from cryptomonitor.exchange_data_etl import run
from cryptomonitor.db import WarehouseConnection
from cryptomonitor.sde_config import get_warehouse_creds


class TestCryptoMonitor:
    def teardown_method(self, test_exchange_data_etl_run):
        with WarehouseConnection(
            get_warehouse_creds()
        ).managed_cursor() as curr:
            curr.execute("TRUNCATE TABLE crypto.exchanges;")

    def get_exchange_data(self):
        with WarehouseConnection(get_warehouse_creds()).managed_cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as curr:
            curr.execute(
                '''SELECT id,
                        name,
                        rank,
                        percenttotalvolume,
                        volumeusd,
                        tradingpairs,
                        socket,
                        exchangeurl,
                        updated_unix_millis,
                        updated_utc
                        FROM crypto.exchanges;'''
            )
            table_data = [dict(r) for r in curr.fetchall()]
        return table_data

    def test_exchange_data_etl_run(self, mocker):
        mocker.patch(
            'cryptomonitor.exchange_data_etl.get_exchange_data',
            return_value=[r for r in csv.DictReader(
                    open('test/fixtures/sample_raw_exchange_data.csv')
                )
            ],
        )
        run()
        expected_result = [
            {
                'id': 'binance',
                'name': 'Binance',
                'rank': 1,
                'percenttotalvolume': Decimal('27.83372'),
                'volumeusd': Decimal('8855176098.0176347673795951'),
                'tradingpairs': 958,
                'socket': True,
                'exchangeurl': 'https://www.binance.com/',
                'updated_unix_millis': 1645444380183,
                'updated_utc': datetime.datetime(
                    2022, 2, 21, 11, 53, 00, 183000
                ),
            },
            {
                'id': 'hitbtc',
                'name': 'HitBTC',
                'rank': 2,
                'percenttotalvolume': Decimal('8.52185'),
                'volumeusd': Decimal('2711189718.7688861002813519'),
                'tradingpairs': 964,
                'socket': True,
                'exchangeurl': 'https://hitbtc.com/',
                'updated_unix_millis': 1645444333475,
                'updated_utc': datetime.datetime(
                    2022, 2, 21, 11, 52, 13, 475000
                ),
            },
            {
                'id': 'okex',
                'name': 'Okex',
                'rank': 3,
                'percenttotalvolume': Decimal('7.02962'),
                'volumeusd': Decimal('2236444161.1450471011310466'),
                'tradingpairs': 422,
                'socket': False,
                'exchangeurl': 'https://www.okex.com/',
                'updated_unix_millis': 1645444379551,
                'updated_utc': datetime.datetime(
                    2022, 2, 21, 11, 52, 59, 551000
                ),
            },
            {
                'id': 'gdax',
                'name': 'Coinbase Pro',
                'rank': 4,
                'percenttotalvolume': Decimal('7.00356'),
                'volumeusd': Decimal('2228152612.8643831291716896'),
                'tradingpairs': 347,
                'socket': True,
                'exchangeurl': 'https://pro.coinbase.com/',
                'updated_unix_millis': 1645444379148,
                'updated_utc': datetime.datetime(
                    2022, 2, 21, 11, 52, 59, 148000
                ),
            },
        ]
        result = self.get_exchange_data()
        assert expected_result == result
