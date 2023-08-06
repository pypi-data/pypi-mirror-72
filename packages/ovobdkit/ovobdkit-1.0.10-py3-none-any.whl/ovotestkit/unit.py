'''
RAW TEST

implementation of simple test case (with less typing)

**how to run?**
```/usr/bin/spark2-submit $(pwd)/raw_test.py```
'''

# import unittest
# import findspark
# findspark.init('/opt/cloudera/parcels/SPARK2/lib/spark2/')

from pyspark.sql import SparkSession
from pyspark.sql.functions import lit,expr, explode, explode_outer, map_values, from_unixtime, unix_timestamp, to_timestamp
from pyspark.sql.types import *
import sys, os
from datetime import datetime,timedelta

import unittest
import logging
from pyspark.sql import SparkSession


class OVOTestKit(unittest.TestCase):
 
    @classmethod
    def suppress_py4j_logging(cls):
        logger = logging.getLogger('py4j')
        logger.setLevel(logging.WARN)

    @classmethod
    def create_testing_pyspark_session(cls):
        return (SparkSession.builder.appName(__name__)\
            .config('hive.exec.dynamic.partition.mode','nonstrict')\
            .enableHiveSupport()\
            .getOrCreate()) 
 
    @classmethod
    def setUpClass(cls):
        cls.suppress_py4j_logging()
        cls.spark = cls.create_testing_pyspark_session()

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def _normalize(self, s):
        return str(s).lower().replace(' ','')

    def field_check(self, table_name, fields, types):
        '''
            table_name : complete table name including db name
            fields : fields from modeller
            types : types from modeller
        '''
        dm_colname = list(map(self._normalize, fields))
        dm_coltype = list(map(self._normalize, types))

        t_struct = self.spark.sql(f"describe {table_name}").toPandas()
        t_struct = t_struct[['col_name','data_type']].to_dict(orient='list')
        t_struct = [ x for x in zip(t_struct['col_name'], t_struct['data_type'])]

        d_struct = [ x for x in zip(list(map(self._normalize, dm_colname)), list(map(self._normalize, dm_coltype)) )]

        self.assertEqual(t_struct, d_struct)
    
    def duplicate_check(self, table_name, columns = ['id']):

        grouper = ','.join(columns)

        Q = f'select {grouper} , count(1) N from {table_name} group by {grouper} having count(1) > 1'
        df = self.spark.sql(Q).toPandas()
        row, col = df.shape

        self.assertEqual(row, 0 , '{} duplicated row found')

    def random_check(self, table_name):
        NotImplementedError()

    def count_check(self, table_name):
        NotImplementedError()

    def hist_count_check(self, table_name):
        NotImplementedError()

