#!/usr/bin/env python3
# Copyright 2020-present NAVER Corp. See LICENSE file for license details

from typing import Union, Dict, List, Tuple, TypeVar, Generic


class RecordWifi:
    """
    RSSI, FREQ, SCANTIME, VISIBLENAME
    """

    def __init__(self,
                 rssi: int,
                 freq: int,
                 scan_time: int,
                 visible_name: str):
        # enforce type
        self.rssi = int(rssi)
        self.freq = int(freq)
        self.scan_time = int(scan_time)
        self.visible_name = str(visible_name)

    def as_list(self) -> List[str]:
        """
        :return: Wifi records as list of strings
        """
        values = [self.rssi, self.freq,
                  self.scan_time, self.visible_name]
        return [str(v) for v in values]

    def __repr__(self) -> str:
        return ', '.join(self.as_list())

    def __hash__(self):
        return hash(tuple(self.as_list()))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.as_list() == other.as_list()


T = TypeVar('T')      # Declare generic type variable


class RecordsBase(Dict[int, Dict[str, T]]):
    """
    brief: Records
            records[timestamp][sensor_id] = <DataRecords>
            or
            records[(timestamp, sensor_id)] = <DataRecords>
    """

    def __setitem__(self,
                    key: Union[int, Tuple[int, str]],
                    value: Union[Dict[str, T], T]):
        """
        Inserts/changes a record.

        :param key: can be timestamp or (timestamp, sensor_id)
        :param value: can be respectively a dict{sensor_id: DataRecords} or DataRecords
        :return:
        """
        # enforce type checking
        if isinstance(key, tuple):
            # key is a pair of (timestamp, device_id)
            timestamp = key[0]
            device_id = key[1]
            if not isinstance(timestamp, int):
                raise TypeError('invalid timestamp')
            if not isinstance(device_id, str):
                raise TypeError('invalid device_id')
            self.setdefault(timestamp, {})[device_id] = value
        elif isinstance(key, int):
            # key is a timestamp
            timestamp = key
            if not isinstance(value, dict):
                raise TypeError('invalid value for data')
            if not all(isinstance(k, str) for k in value.keys()):
                raise TypeError('invalid device_id')
            super(RecordsBase, self).__setitem__(timestamp, value)
        else:
            raise TypeError('key must be Union[int, Tuple[int, str]]')

    def __getitem__(self, key: Union[int, Tuple[int, str]]) -> Union[Dict[str, T], T]:
        """
        Returns a single record for a (timestamp, sensor) or all records for a timestamp.

        :param key: can be timestamp or (timestamp, sensor_id)
        :return: return respectively a dict{sensor_id: DataRecords} or DataRecords
        """
        if isinstance(key, tuple):
            # key is a pair of (timestamp, device_id)
            timestamp = key[0]
            device_id = key[1]
            if not isinstance(timestamp, int):
                raise TypeError('invalid timestamp')
            if not isinstance(device_id, str):
                raise TypeError('invalid device_id')
            return super(RecordsBase, self).__getitem__(timestamp)[device_id]
        elif isinstance(key, int):
            # key is a timestamp
            return super(RecordsBase, self).__getitem__(key)
        else:
            raise TypeError('key must be Union[int, Tuple[int, str]]')

    def key_pairs(self) -> List[Tuple[int, str]]:
        """
        Returns a list of (timestamp, device_id) contained in records.
        Those pairs can be used to access a single record data.

        :return: list of (timestamp, device_id)
        """
        return [
            (timestamp, sensor_id)
            for timestamp, sensors in self.items()
            for sensor_id in sensors.keys()
        ]

    def __contains__(self, key:  Union[int, Tuple[int, str]]):
        if isinstance(key, tuple):
            # key is a pair of (timestamp, device_id)
            timestamp = key[0]
            device_id = key[1]
            if not isinstance(timestamp, int):
                raise TypeError('invalid timestamp')
            if not isinstance(device_id, str):
                raise TypeError('invalid device_id')
            return super(RecordsBase, self).__contains__(timestamp) and device_id in self[timestamp]
        elif isinstance(key, int):
            return super(RecordsBase, self).__contains__(key)
        else:
            raise TypeError('key must be Union[int, Tuple[int, str]]')

    def __repr__(self) -> str:
        # [timestamp, sensor_id] = str
        lines = [f'[ {timestamp:010}, {sensor_id:5}] = {data}'
                 for timestamp, sensors in self.items()
                 for sensor_id, data in sensors.items()]
        return '\n'.join(lines)


class RecordsCamera(RecordsBase[str]):
    """
    Camera records
    """
    def __setitem__(self,
                    key: Union[int, Tuple[int, str]],
                    value: Union[Dict[str, str], str]):
        """ see RecordsBase.__setitem__ """
        if isinstance(key, tuple):
            if not isinstance(value, str):
                raise TypeError('invalid data')
        elif isinstance(key, int):
            if not isinstance(value, dict):
                raise TypeError('invalid value for data')
            if not all(isinstance(v, str) for v in value.values()):
                raise TypeError('invalid data')
        super(RecordsCamera, self).__setitem__(key, value)


class RecordsLidar(RecordsBase[str]):
    """
    Lidar records
    """
    def __setitem__(self,
                    key: Union[int, Tuple[int, str]],
                    value: Union[Dict[str, str], str]):
        """ see RecordsBase.__setitem__ """
        if isinstance(key, tuple):
            if not isinstance(value, str):
                raise TypeError('invalid data')
        elif isinstance(key, int):
            if not isinstance(value, dict):
                raise TypeError('invalid value for data')
            if not all(isinstance(v, str) for v in value.values()):
                raise TypeError('invalid data')
        super(RecordsLidar, self).__setitem__(key, value)


class RecordsWifi(RecordsBase[Dict[str, RecordWifi]]):
    """
    brief: Records
            records[timestamp][sensor_id][bssid] = <RecordWifi>
            or
            records[(timestamp, sensor_id)][bssid] = <RecordWifi>
    """

    def __setitem__(self,
                    key: Union[int, Tuple[int, str]],
                    value: Dict[str, RecordWifi]):
        if isinstance(key, tuple):
            if not isinstance(value, Dict):
                raise TypeError('invalid data')
        elif isinstance(key, int):
            if not isinstance(value, dict):
                raise TypeError('invalid value for data')
            if not all(isinstance(v, dict) for v in value.values()):
                raise TypeError('invalid data')
        super(RecordsWifi, self).__setitem__(key, value)
