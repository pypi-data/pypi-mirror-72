
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

    SRC_DS : DataSource = None
    DST_DS : DataSource = None
    DST_TABLE: str = None
    SRC_TABLE: str = None

    '''
        schema : 
        normally just do 

        field1 type1
        field2 type2
        field3 type3

        example : 
            id  int
            name string
            date_created timestamp

        for structure with partition:
            id              int
            name            string 
            date_created    timestamp
            date_partition  string  *partition

        field having 3 columns read as partition.
    '''
    SRC_SCHEMA: str = None
    DST_SCHEMA: str = None

    '''
        fields expects following structure :

        field0 , type0 
        field1 , type1
        field2 , type2
        field3 , type3
    '''
    FIELDS = '''
        `id` BigInt
        `name` String
    '''

    PARTITION = '''
        `date_partition` String
    '''

    def __repr__(self):
        info = f'''\
TABLE NAME : 
    {BaseETL.SRC_TABLE}
Fields : 
    {BaseETL.SRC_SCHEMA.strip()}
Partition:
    {BaseETL.PARTITION.strip()}
Stored As : Parquet
TABLE PROPERTIES : 
    "parquet.compression" : "SNAPPY"
        '''
        return info

    def __init__(self,*args, **kwargs):

        super(BaseETL, self).__init__()
        # self._props = {}
        setattr(self,'_props',{})

        self._src_fields = None
        self._src_types = None
        self._dst_fields = None
        self._dst_types = None
        self._augmented_fields = None
        self._partitions = None
        self.spark = None

        keys = kwargs.keys()
        self._proc_columns = None
        for key in keys:
            self._props[key] = kwargs[key]
            # setattr(self, key, kwargs[key])

        if self.spark is None:
            self.setUp()

    def __getattr__(self, name):
        # return getattr(self,name)
        return self._props[name]
    
    # def __setattr__(self, name, value):
    #     self._props[name] = value
        # setattr(self, name, value)
    
    @property
    def partitions(self):
        return self._partitions
    
    @property
    def source_table(self):
        return f"{self.SRC_TABLE}"

    @property
    def columns(self):
        if self._proc_columns is None:
            self._proc_columns = self._process_columns()
        return self._proc_columns

    def _process_columns(self):

        self._check_fields()

        self._src_fields = list(self._extract_fields(self.SRC_SCHEMA))
        self._src_types = list(self._extract_types(self.SRC_SCHEMA))

        self._dst_fields = list(self._extract_fields(self.DST_SCHEMA))
        self._dst_types = list(self._extract_types(self.DST_SCHEMA))

        MAX = len(self._src_fields)
        L = []

        for i in range(MAX):
            src_type = self._src_types[i]
            dst_type = self._dst_types[i]
            field_def = self._src_fields[i]

            # print(field_def, src_type, dst_type)
            if src_type != dst_type:
                if dst_type == 'timestamp':
                    field_def = f'cast( from_unixtime({field_def}/1000) as {dst_type}) {field_def}'
                else:
                    field_def = f'cast({field_def} as {dst_type})'

            L.append(field_def)
        
        return ','.join(L)

    def _set_partition_field(self, field_name:str):
        if self._partitions is None:
            self._partitions = []

        self._partitions.append(field_name)

    def _extract_fields(self , SCHEMA:str):
        defs = self._extract_definitions(SCHEMA)
        for field in defs:
            f = field.strip().split(' ')
            if len(f) > 2:
                self._set_partition_field(f[0].lower())
            yield f[0].lower()

    def _extract_types(self , SCHEMA:str):
        defs = self._extract_definitions(SCHEMA)
        for field in defs:
            f = field.strip().split(' ')
            if len(f) > 2:
                self._set_partition_type(f[1].lower())
            yield f[1].lower()

    def _extract_definitions(self, SCHEMA: str):
        for field in SCHEMA.strip().split('\n'):
            yield field

    @property
    def destination_table(self):
        return f'{self.DST_TABLE}'
    
    @property
    def all_fields(self):
        return self._all_fields()

    @property
    def source_schema(self):
        return

    @property 
    def destination_schema(self):
        return

    def _check_fields(self):
        if not hasattr(self, 'SRC_TABLE'):
            raise Exception('field SRC_TABLE is required')
        if not hasattr(self, 'DST_TABLE'):
            raise Exception('field DST_TABLE is required')
        if not hasattr(self, 'SRC_SCHEMA'):
            raise Exception('field SRC_SCHEMA is required')
        if not hasattr(self, 'DST_SCHEMA'):
            raise Exception('field DST_SCHEMA is required')

    def _get_fields(self):
        return ', '.join([line.strip() for line in BaseETL.FIELDS.strip().split('\n')])

    def _parse_fields(self, field_def: str):
        return ', '.join([line.strip() for line in field_def.strip().split('\n')])

    def  _get_partitions(self):
        return ', '.join([line.strip() for line in BaseETL.PARTITION.strip().split('\n')])

    def _all_fields(self):
        _fields = [line.strip() for line in BaseETL.FIELDS.strip().split('\n')] + [line.strip() for line in BaseETL.PARTITION.strip().split('\n')]
        return ', '.join(_fields)

    @property
    def augmented_fields(self):
        if self._src_fields is None or self._dst_fields is None:
            self._process_columns()
        
        if self._augmented_fields is None:
            self._augmented_fields = [ e for e in self._dst_fields if e not in self._src_fields ]

        return self._augmented_fields
    
    @property
    def src_fields(self):
        if self._src_fields is None :
            self._process_columns()
        L = []
        for  o in zip(self._src_fields, self._src_types):
            field, typ = o
            L.append(f'{field} {typ}')
        return ','.join(L)
    
    @property
    def partition_fields(self):
        if self._src_fields is None:
            self._process_columns()
        L = []
        for o in zip(self._partition_fields, self._partition_types):
            f, t = o 
            L.append(f'{f} {t}')
        return ','.join(L)


    @property
    def dst_fields(self):
        if self._src_fields is None :
            self._process_columns()
        L = []
        for  o in zip(self._dst_fields, self._dst_types):
            
            field, typ = o
            L.append(f'{field} {typ}')
        return ','.join(L)
    
    @property
    def src_fields_list(self):
        if self._src_fields is None :
            self._process_columns()
        return self._src_fields

    @property
    def src_types_list(self):
        if self._src_types is None :
            self._process_columns()
        return self._src_types

    @property
    def dst_fields_list(self):
        if self._dst_fields is None :
            self._process_columns()
        return self._dst_fields

    @property
    def dst_types_list(self):
        if self._dst_types is None :
            self._process_columns()
        return self._dst_types


    def create_src_table_stmt(self):
        partition_stmt = ''

        if self.partitions is not None:
            partition_stmt = ','.join(self.partition_fields)

        return f"""CREATE TABLE {self.source_table} (
                    {self.src_fields}
                ) {partition_stmt} 
                STORED AS PARQUET  
                TBLPROPERTIES ("parquet.compression" = "SNAPPY" )
                """

    def create_dst_table_stmt(self):
        partition_stmt = ''

        return f"""CREATE TABLE {self.destination_table} (
                    {self.dst_fields}
                ) {partition_stmt} 
                STORED AS PARQUET  
                TBLPROPERTIES ("parquet.compression" = "SNAPPY" )
                """
    @abc.abstractmethod
    def setUp(self):
        '''
            override this if other settings required for your 
            task
        '''
        raise NotImplementedError("set up has to be implemented")

    def tearDown(self):
        self.spark.stop()

    @abc.abstractmethod
    def extract(self):
        pass

    @abc.abstractmethod
    def transform(self):
        '''
            self.spark is available.
        '''
        raise NotImplementedError("this method should be overriden and implemented")
    
    @abc.abstractmethod
    def load(self):
        pass

    def create_src_table(self):
        if self.SRC_DS != DataSource.HIVE:
            raise Exception("Cannot create table on non HIVE data source")
        stmt = self.create_src_table_stmt()
        self.spark.sql(stmt)

    def create_dst_table(self):
        if self.DST_DS != DataSource.HIVE:
            raise Exception("Cannot create table on non HIVE data source")

        stmt = self.create_dst_table_stmt()
        self.spark.sql(stmt)

    def truncate_src_table(self):
        Q = f'''truncate table {self.source_table}'''
        self.spark.sql(Q)

    def truncate_dst_table(self):
        Q = f'''truncate table {self.destination_table}'''
        self.spark.sql(Q)

    def run(self):
        self.setUp()
        self.extract()
        self.transform()
        self.load()
        self.tearDown()