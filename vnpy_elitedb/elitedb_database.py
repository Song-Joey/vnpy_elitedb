from typing import List, Optional
from datetime import datetime
from pathlib import Path
import shelve

import pandas as pd
import pyarrow as pa
import numpy as np

from vnpy.trader.database import BaseDatabase, BarOverview, TickOverview, DB_TZ
from vnpy.trader.object import BarData, TickData, ContractData
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.utility import get_file_path


path: Path = get_file_path("elite_db")


class ElitedbDatabase(BaseDatabase):
    """VeighNa EliteDB数据库接口"""

    def __init__(self) -> None:
        """"""
        pass

    def delete_bar_data(
        self,
        symbol: str,
        exchange: Exchange,
        interval: Interval
    ) -> int:
        """删除K线数据"""
        pass

    def delete_tick_data(
        self,
        symbol: str,
        exchange: Exchange
    ) -> int:
        """删除TICK数据"""
        pass

    def get_bar_overview(self) -> List[BarOverview]:
        """查询数据库中的K线汇总信息"""
        file_path: str = str(path.joinpath("bar_overview"))
        with shelve.open(file_path) as data:
            values = list(data.values())
        return [BarOverview(**item) for item in values]

    def get_tick_overview(self) -> List[TickOverview]:
        """查询数据库中的Tick汇总信息"""
        pass

    def load_bar_data(
        self,
        symbol: str,
        exchange: Exchange,
        interval: Interval,
        start: datetime,
        end: datetime
    ) -> List[BarData]:
        """读取K线数据"""
        df = self.load_bar_df(symbol, exchange, interval, start, end)
        if df is None:
            return []

        if df.empty:
            return []

        data = df.to_numpy()
        return [BarData(*row) for row in data]

    @ staticmethod
    def load_bar_df(
        symbol: str,
        exchange: Exchange,
        interval: Interval,
        start: datetime,
        end: datetime
    ) -> Optional[pd.DataFrame]:
        """读取K线数据"""
        file_name: str = f"{symbol}_{exchange.value}_{interval.value}"
        file_path: str = str(path.joinpath(file_name))

        try:
            df: pd.DataFrame = pa.ipc.open_file(file_path).read_pandas()
        except FileNotFoundError:
            return None

        df = df[(df["datetime"] >= start) & (df["datetime"] <= end)]
        df["exchange"] = df["exchange"].apply(Exchange)
        df["interval"] = df["interval"].apply(Interval)
        df["datetime"] = df["datetime"].dt.tz_localize(DB_TZ)
        df.insert(0, "gateway_name", "DB")
        df.index = df["datetime"]
        return df

    @ staticmethod
    def load_contract_data() -> List[ContractData]:
        """加载合约数据"""
        file_path: str = str(path.joinpath("contract_data"))
        with shelve.open(file_path) as data:
            values = list(data.values())
        return values

    def load_tick_data(
        self,
        symbol: str,
        exchange: Exchange,
        start: datetime,
        end: datetime
    ) -> List[TickData]:
        """读取TICK数据"""
        pass

    def load_tick_df(
        self,
        symbol: str,
        exchange: Exchange,
        start: datetime,
        end: datetime
    ) -> Optional[pd.DataFrame]:
        """读取TICK数据"""
        pass

    def save_bar_data(self, bars: List[BarData], stream: bool = False) -> bool:
        """保存K线数据"""
        pass

    def save_contract_data(self, contracts: List[ContractData], stream: bool = False) -> bool:
        """保存合约数据"""
        pass

    def save_tick_data(self, ticks: List[TickData], stream: bool = False) -> bool:
        """保存TICK数据"""
        pass
