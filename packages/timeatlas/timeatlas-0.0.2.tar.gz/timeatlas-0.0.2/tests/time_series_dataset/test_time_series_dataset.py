from unittest import TestCase
from timeatlas import TimeSeriesDataset
import timeatlas as ta


class TestTimeSeriesDataset(TestCase):

    def setUp(self) -> None:
        self.target_dir = "../data/test-import/to_text_without_metadata"
        self.my_time_series_1 = ta.read_text(self.target_dir)
        self.my_time_series_2 = ta.read_text(self.target_dir)

    def test__TimeSeriesDataset__is_instance(self):
        my_time_series_dataset = TimeSeriesDataset()
        self.assertIsInstance(my_time_series_dataset, TimeSeriesDataset)

    def test__TimeSeriesDataset__construct(self):
        my_arr = [self.my_time_series_1, self.my_time_series_2]
        my_time_series_dataset = TimeSeriesDataset(my_arr)
        self.assertTrue(my_time_series_dataset.len() == 2)
        self.assertIsInstance(my_time_series_dataset, TimeSeriesDataset)

    def test__TimeSeriesDataset__add(self):
        tsd = TimeSeriesDataset()
        self.assertTrue(tsd.len() == 0)
        tsd.add(self.my_time_series_1)
        self.assertTrue(tsd.len() == 1)
        tsd.add(self.my_time_series_2)
        self.assertTrue(tsd.len() == 2)

    def test__TimeSeriesDataset__remove(self):
        my_arr = [self.my_time_series_1, self.my_time_series_2]
        tsd = TimeSeriesDataset(my_arr)
        self.assertTrue(tsd.len() == 2)
        tsd.remove(-1)
        self.assertTrue(tsd.len() == 1)
        tsd.remove(-1)
        self.assertTrue(tsd.len() == 0)
