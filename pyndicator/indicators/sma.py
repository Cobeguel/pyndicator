from dataclasses import dataclass, field

from pyndicator.types.candlestick import OHLCV, CandleComponent
from pyndicator.indicators.base import Indicator
from pyndicator.types.candlestick import OHLCV

import logging

@dataclass
class SMA(Indicator):
    component: CandleComponent = field(default=CandleComponent.CLOSE)
    cumulative: float = 0.0

    def initialize(self):
        for data in self.data:
            self.cumulative += data.getComponent(self.component)
            logging.debug(data.getComponent(self.component))
        self.values.appendleft(self.cumulative/self.periods)

    def next_value(self, old_data: OHLCV):
        self.cumulative -= old_data.getComponent(self.component)
        self.cumulative += self.data[0].getComponent(self.component)
        self.values[0] = self.cumulative/self.periods

    def rebase(self, old_data: OHLCV):
        self.cumulative -= old_data.getComponent(self.component)
        self.cumulative += self.data[0].getComponent(self.component)
        self.values.appendleft(self.cumulative/self.periods)
