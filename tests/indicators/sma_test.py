import unittest

from pyndicator.types.candlestick import OHLCV, CandleComponent
from pyndicator.types.time import Resolutions, TimeIndex
from pyndicator.indicators.sma import SMA

class TestSMA(unittest.TestCase):

    def test_sma_initialization(self):
        ohlc_data = [OHLCV(close=i) for i in range(100)]
        sma = SMA(periods=10, label="foo", resolution=Resolutions.minutes_1, window_size=5, data_list=ohlc_data)

        expected_sma = sum([data.getComponent(CandleComponent.CLOSE) for data in ohlc_data[-10:]]) / 10
        assert sma.value == expected_sma

    def test_sma_next_value(self):
        ohlc_data = [OHLCV(...) for _ in range(100)]
        sma = SMA(periods=10, label="foo", resolution=Resolutions.minutes_1, window_size=5, data_list=ohlc_data)

        new_data = OHLCV(...)
        sma.next(new_data, TimeIndex(30)) 

        expected_sma = sum([data.getComponent(CandleComponent.CLOSE) for data in list(sma.data)[:10]]) / 10
        assert sma.value == expected_sma

    def test_sma_rebase(self):
        ohlc_data = [OHLCV(...) for _ in range(100)]
        sma = SMA(periods=10, label="foo", resolution=Resolutions.minutes_1, window_size=5, data_list=ohlc_data)

        new_data = OHLCV(...)
        sma.next(new_data, TimeIndex(60)) 

        expected_sma = sum([data.getComponent(CandleComponent.CLOSE) for data in list(sma.data)[:10]]) / 10
        assert sma.value == expected_sma
