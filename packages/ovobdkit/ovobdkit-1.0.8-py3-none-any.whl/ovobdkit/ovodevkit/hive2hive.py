from .base_task import BaseETL
from .base_task import DataSource
from pyspark.sql import SparkSession
import sys

class Hive2HiveEtl(BaseETL):
    SRC_DS = DataSource.HIVE
    DST_DS = DataSource.HIVE
    spark = None

    def __init__(self, *args, **kwargs):
        super(Hive2HiveEtl,self).__init__(*args,**kwargs)

    def getSpark(self):
        if self.spark is None:
            self.spark = SparkSession.builder.appName(__name__)\
                            .enableHiveSupport()\
                            .getOrCreate()

        return self.spark