from .base_task import BaseETL
from .base_task import DataSource
from pyspark.sql import SparkSession
import sys

class Hive2HiveEtl(BaseETL):
    SRC_DS = DataSource.HIVE
    DST_DS = DataSource.HIVE

    def __init__(self, *args, **kwargs):
        super(Hive2HiveEtl,self).__init__(*args,**kwargs)

    def setUp(self):
        self.spark = SparkSession.builder.appName(__name__)\
                        .enableHiveSupport()\
                        .getOrCreate()