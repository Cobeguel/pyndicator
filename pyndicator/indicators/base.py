from abc import ABC, abstractmethod
from dataclasses import dataclass, field, InitVar
from collections import deque
from typing import Deque, List

from pyndicator.types.candlestick import OHLCV
from pyndicator.types.time import Resolutions, TimeIndex

@dataclass
class Indicator(ABC):
    label: str
    resolution: Resolutions
    periods: int
    window_size: int
    data: Deque[OHLCV] = field(default=None, init=False)
    values: Deque[float] = field(default=None, init=False)
    _rebase: bool = field(default=False, init=False)
    resolution_index: TimeIndex = field(default_factory=lambda: TimeIndex(None), init=False)
    last_data: OHLCV = field(default_factory=OHLCV, init=False)

    data_list: InitVar[List[OHLCV]] # Needed to extend the signature of the __init__ method
    
    def __post_init__(self, data_list: List[OHLCV]):
        if self.periods < 0:
            raise ValueError("size must be positive")
        if self.window_size < 0:
            raise ValueError("window_size must be positive")
        if len(data_list) < self.window_size:
            raise ValueError("data_list must have at least window_size elements")

        self.data = deque(data_list[-self.periods:], maxlen=self.periods)
        self.values = deque(maxlen=self.window_size)
        self.resolution_index = TimeIndex(self.resolution.value)
        self.initialize()
        

    def next(self, data: OHLCV, candletime: TimeIndex):
        if len(self.data) < self.periods:
            self.data.appendleft(data)

        if candletime % self.resolution_index != 0:
            self.data[0] = data
            self.next_value()
        else: 
            self.data.appendleft(data)
            self.rebase()

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def next_value(self):
        pass

    @abstractmethod
    def rebase(self):
        pass

    @property
    def value(self) -> float:
        return self.values[0] if self.values else 0.0
