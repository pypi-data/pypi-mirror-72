
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit,expr, explode, explode_outer, map_values, from_unixtime, unix_timestamp, to_timestamp
from pyspark.sql.types import *
from enum import Enum
import sys, os
from datetime import datetime,timedelta
import abc

class DataSource(Enum):
    HIVE = 'HIVE'
    MYSQL = 'MYSQL'
    PGSQL = 'PGSQL'

HIVE_TYPES=[
        r'TINYINT',r'SMALLINT',r'INT',
        r'INTEGER',r'BIGINT',r'FLOAT',r'DOUBLE',
        r'DOUBLE\s+PRECISION',r'DECIMAL\s+\(\d{,2}(\,\d{,2})?\)',
        r'TIMESTAMP',r'DATE',r'INTERVAL',r'STRING',r'VARCHAR\s+\(\d{,2}\)',r'CHAR\s+\(\d{,2}\)',
        r'BOOLEAN',r'BINARY'
    ]

class BaseETL:
    __metaclass__ = abc.ABCMeta

    def __init__(self,*args, **kwargs):
        super(BaseETL, self).__init__()

    @abc.abstractmethod
    def transform(self):
        '''
            self.spark is available.
        '''
        raise NotImplementedError("this method should be overriden and implemented")

    def run(self):
        self.transform()