from typing import NoReturn, Union
from timeatlas import TimeSeries
from pandas import DataFrame
import fbprophet as fbp

from timeatlas.abstract import AbstractBaseModel


class Prophet(AbstractBaseModel):

    def __init__(self):
        super().__init__()
        self.model = fbp.Prophet()

    def fit(self, series) -> NoReturn:
        super().fit(series)
        df = self.__prepare_series_for_prophet(self.X_train)
        self.model.fit(df)

    def predict(self, horizon: Union[str, TimeSeries], freq: str = None) -> TimeSeries:
        super().predict(horizon)
        if isinstance(horizon, str):
            future = self.make_future_dataframe(horizon, freq)
        elif isinstance(horizon, TimeSeries):
            future = self.__prepare_series_for_prophet(horizon.erase())
        forecast = self.model.predict(future)
        return TimeSeries.from_df(forecast, 'yhat', 'ds')

    @staticmethod
    def __prepare_series_for_prophet(series: TimeSeries):
        df = series.to_df()
        df["ds"] = df.index
        df = df.reset_index(drop=True)
        df = df.rename(columns={"values": "y"})
        return df

    def make_future_dataframe(self, horizon: str, freq: str = None):
        index = self.make_future_index(horizon, freq)
        df = DataFrame(data=index.to_series(), columns=["ds"])
        df = df.reset_index(drop=True)
        return df
