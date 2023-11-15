from dataclasses import dataclass, field

from pyndicator.types.candlestick import OHLCV, CandleComponent
from pyndicator.indicators.base import Indicator
from pyndicator.types.candlestick import OHLCV

@dataclass
class SMA(Indicator):
    component: CandleComponent = field(default=CandleComponent.CLOSE)
    cumulative: float = 0.0

    lastCandle: OHLCV = field(default_factory=OHLCV, init=False)

    def initialize(self):
        for data in self.data:
            self.cumulative += data.getComponent(self.component)
        self.values.appendleft(self.cumulative/self.periods)
        self.lastCandle = self.data[-1]

    def next_value(self):
        self.cumulative -= self.lastCandle.getComponent(self.component)
        self.cumulative += self.data[0].getComponent(self.component)
        self.values[0] = self.cumulative/self.periods

    def rebase(self):
        self.cumulative -= self.lastCandle.getComponent(self.component)
        self.cumulative += self.data[0].getComponent(self.component)
        self.values.appendleft(self.cumulative/self.periods)
        self.lastCandle = self.data[-1]
