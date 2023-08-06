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
from random import seed
from random import randint
import pandas as pd

import unittest
import logging
from pyspark.sql import SparkSession

from typing import List, Tuple
from bash import bash


class OVOTestKit(unittest.TestCase):
    TABLE: str = None
    FIELDS: str = None
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
        logging.basicConfig()
        cls.log = logging.getLogger("LOG")

        cls.suppress_py4j_logging()
        cls.spark = cls.create_testing_pyspark_session()

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def getSpark(self) -> SparkSession:
        return OVOTestKit.create_testing_pyspark_session()

    # @property
    # def spark(self) -> SparkSession :
    #     cls = self.__class__
    #     return cls.spark

    def _normalize(self, s):
        return str(s).lower().replace(' ','')

    def field_check(self, table_name:str, fields: List[str], types: List[str]):
        '''
            table_name : complete table name including db name
            fields : fields from modeller
            types : types from modeller
        '''
        self.spark = self.getSpark()
        dm_colname = list(map(self._normalize, fields))
        dm_coltype = list(map(self._normalize, types))

        t_struct = self.spark.sql(f"describe {table_name}").toPandas()
        t_struct = t_struct[['col_name','data_type']].to_dict(orient='list')
        t_struct = [ x for x in zip(t_struct['col_name'], t_struct['data_type'])]

        d_struct = [ x for x in zip(list(map(self._normalize, dm_colname)), list(map(self._normalize, dm_coltype)) )]

        self.assertEqual(t_struct, d_struct)
    
    def duplicate_check(self, table_name, columns = ['id']):
        self.spark = self.getSpark()
        grouper = ','.join(columns)

        Q = f'select {grouper} , count(1) N from {table_name} group by {grouper} having count(1) > 1'
        df = self.spark.sql(Q).toPandas()
        row, col = df.shape

        self.assertEqual(row, 0 , '{} duplicated row found')

    def random_check(self, table_name:str,fields:str,order_by:str, pick_indexes: List[int], compare_with: pd.DataFrame ):
        idx = pick_indexes
        ref = compare_with
        self.spark = self.getSpark()
        Q = f'select {fields} from {table_name} order by {order_by} limit 1000 '
        df = self.spark.sql(Q).toPandas()
        #check index less than 1000
        
        if len(idx) > 5:
            raise Exception("length should be less than equals to 5")

        over_range = [ i for i in idx if i > 1000]
        if len(over_range) > 0 :
            raise Exception("we found index larger than maximum: 1000")

        #find sample by index
        samples = df.loc[idx].to_records(index=False).tolist()
        comparison = ref.loc[idx].to_records(index=False).tolist()
        # self.assertEqual(samples, comparison)
        for o in zip(samples, comparison):
            L, R = o 
            print("COMPARING L :\n", L, "\n\nWITH R :\n", R)
            self.assertEqual(L,R)
        
        # NotImplementedError()

    def count_check(self, table_name, ref):
        self.spark = self.getSpark()
        if ref < 1:
            raise Exception("count sould be greather or equal to 1")
        Q = f'select count(1) N from {table_name}'
        df = self.spark.sql(Q).toPandas()

        self.assertEqual(df['N'][0], ref)

    @property
    def table(self):
        return self.TABLE

class ImpalaShell:
    @classmethod
    def getShowCreateTable(cls, table_name):
        b = bash(f"impala-shell -i bddevdn0001.bigdata.ovo.id -d default -k -q 'show create table {table_name}'")
        out = b.stdout
        return out.decode('utf-8')