from datetime import datetime, timezone
from enum import Enum
from dataclasses import dataclass, field
from collections import deque
from abc import ABC, abstractmethod
from typing import Deque

class TimeResolution(Enum):
    SECOND = 1
    MILLISECOND = 2
    MICROSECOND = 3

@dataclass
class TimeIndex:
    timestamp: int

    def _update(self, timestamp: int):
        if self._is_Valid(timestamp):
            self.timestamp = timestamp

    def _is_Valid(self, timestamp: int):
        if timestamp < 0:
            raise ValueError("Timestamp must be positive: ", timestamp)

        try:
            date = datetime.utcfromtimestamp(timestamp)
            return True
        except ValueError:
            raise ValueError("Invalid timestamp: ", timestamp)


    @classmethod
    def from_datetime(cls, dt: datetime):
        if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
            dt = dt.replace(tzinfo=timezone.utc)
        
        return cls(int(dt.timestamp()))
    
    def update_from_timestamp(self, time: int):
        self._update(time)

    def update_from_datetime(self, dt: datetime):
        if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
            dt = dt.replace(tzinfo=timezone.utc)
    
        self._update(int(dt.timestamp()))


class CandleComponent(Enum):
    OPEN = "open"
    HIGH = "high"
    LOW = "low"
    CLOSE = "close"
    VOLUME = "volume"

@dataclass
class OHLCV:
    open: float = 0.0
    high: float = 0.0
    low: float = 0.0
    close: float = 0.0
    volume: int = 0.0

    def getComponent(self, component: CandleComponent):
        if component == CandleComponent.OPEN:
            return self.open
        elif component == CandleComponent.CLOSE:
            return self.close
        elif component == CandleComponent.HIGH:
            return self.high
        elif component == CandleComponent.LOW:
            return self.low
        elif component == CandleComponent.VOLUME:
            return self.volume
        else:
            raise ValueError("Invalid component: ", component)







    


