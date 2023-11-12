from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timezone
from abc import ABC, abstractmethod

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
        try:
            date = datetime.datetime.utcfromtimestamp(timestamp)
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

    def __mod__(self, t: "TimeIndex"):
        return self.timestamp % t.timestamp
    

class Resolutions(Enum):
    seconds_1 = 1
    seconds_5 = 5
    seconds_15 = 15
    seconds_30 = 30
    minutes_1 = 60
    minutes_3 = 180
    minutes_5 = 300
    minutes_10 = 600
    minutes_15 = 900
    minutes_30 = 1800
    hours_1 = 3600
    hours_2 = 7200
    hours_4 = 14400
    hours_6 = 21600
    hours_8 = 28800
    hours_12 = 43200
    day = 86400
    week = 604800 
