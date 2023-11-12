import unittest
from datetime import datetime, timezone
from pyndicator.types.candlestick import TimeIndex

class TestTimeIndex(unittest.TestCase):

    def test_is_valid_timestamp(self):
        valid_timestamp = 1632492957
        time_index = TimeIndex(valid_timestamp)
        self.assertTrue(time_index._is_Valid(valid_timestamp))

    def test_is_invalid_timestamp(self):
        with self.assertRaises(ValueError):
            invalid_timestamp = -1
            time_index = TimeIndex(invalid_timestamp)
            time_index._is_Valid(invalid_timestamp)

    def test_update_from_timestamp(self):
        time_index = TimeIndex(1632492957)
        new_timestamp = 1632492958
        time_index.update_from_timestamp(new_timestamp)
        self.assertEqual(time_index.timestamp, new_timestamp)

    def test_from_datetime(self):
        dt = datetime(2021, 9, 24, tzinfo=timezone.utc)
        time_index = TimeIndex.from_datetime(dt)
        self.assertEqual(time_index.timestamp, int(dt.timestamp()))

    def test_update_from_datetime(self):
        time_index = TimeIndex(1632492957)
        new_dt = datetime(2021, 9, 25, tzinfo=timezone.utc)
        time_index.update_from_datetime(new_dt)
        self.assertEqual(time_index.timestamp, int(new_dt.timestamp()))
