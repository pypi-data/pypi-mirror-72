from .base_task import BaseETL
from .base_task import DataSource
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit,expr, explode, explode_outer, map_values, from_unixtime, unix_timestamp, to_timestamp
from pyspark.sql.types import *


class Mysql2HiveEtl(BaseETL):
    SRC_DS = DataSource.MYSQL
    DST_DS = DataSource.HIVE
    SRC_TABLE = ''
    DST_TABLE = ''
    SRC_SCHEMA  = ''
    DST_SCHEMA = ''

    def setUp(self):
        self._spark = SparkSession.builder.appName(__name__)\
        .config('spark.jars.packages','mysql:mysql-connector-java:8.0.17')\
        .config("parquet.compression", "SNAPPY")\
        .enableHiveSupport()\
        .getOrCreate()

    def extract(self):
        url = "jdbc:mysql://{host}:{port}/{db}".format(
            host=self.host,port=self.port,db=self.db
        )
        self.df0 = self.spark.read.format('jdbc')\
            .option('serverTimezone','Asia/Jakarta')\
            .option('url',url)\
            .option('dbtable', self.SRC_TABLE )\
            .option("driver", "com.mysql.jdbc.Driver")\
            .option('user',self.username)\
            .option('password',self.password).load()

    def transform(self):
        self.df0 = self.df0.withColumn('PPN_DTTM', to_timestamp(lit(self.ppn_dttm),'yyyy-MM-dd HH:mm:ss'))\
            .withColumn('JOB_ID', lit(self.job_id))

    def load(self):
        self.spark.sql('drop table if exists {temp_table}'.format(temp_table=self.temp_table))
        self.df0.write.format('parquet').option('mode','overwrite').saveAsTable(self.temp_table)

        Q1 = '''insert overwrite table {raw_table} partition (PRC_DT='{prc_dt}') select * from {temp_table}'''.format(
            temp_table=self.temp_table, 
            prc_dt= self.prc_dt,
            raw_table=self.DST_TABLE
        )
        self.spark.sql(Q1)