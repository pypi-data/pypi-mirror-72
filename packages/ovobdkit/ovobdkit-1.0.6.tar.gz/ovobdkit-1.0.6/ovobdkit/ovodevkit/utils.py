import re
import logging
from collections import OrderedDict
from typing import Tuple

logger = logging.getLogger()

class FieldDefinition(OrderedDict):
    def __init__(self, *args , **kwargs):
        super(FieldDefinition, self).__init__(*args, **kwargs)
    
    def __str__(self):
        return ', '.join([ f'{k} {v}' for k, v in zip(self.keys(), self.values())])
    
    def __add__(self, other):
        # print(other)
        for k, v in  zip(other.keys(), other.values()):
            self[k] = v
        return self

    def __eq__(self, other):
        return str(self).lower() == str(other).lower()

class FieldList(list):
    def __init__(self,):
        super(FieldList, self).__init__()
    def __str__(self):
        return ', '.join([ v for v in self ])

class Utils:
    @classmethod
    def parse_schema(cls, schema: str) -> Tuple[FieldDefinition, FieldDefinition]:

        s = schema.strip()
        space = re.compile(r'\s+')
        fields = FieldDefinition()
        partitions = FieldDefinition()
        logger.info(f"stripped schema : {s}")
        for line in s.split("\n"):
            defline = space.split(line.strip())
            if len(defline) < 2:
                logger.error("definition line less than 2")
            if defline[-1] == '*':
                partitions[defline[0]] = ' '.join(defline[1:-1])
                logger.info("flagged as partition")
            else:
                #usual field
                fields[defline[0]] = ' '.join(defline[1:])
        
        return fields, partitions
    @classmethod
    def convert_fields(cls, src: FieldDefinition , tgt: FieldDefinition) -> str:
        '''
            converting fields. 
                note: currently only support field rename
        '''
        src_fields = src.keys()
        src_dtype = src.values()

        tgt_fields = tgt.keys()
        tgt_dtype = tgt.values()

        return ','.join([f'{sfield} {tfield}' for sfield, tfield in zip(src_fields, tgt_fields)])

    @classmethod
    def create_table_statement(cls, table_name: str, fields: OrderedDict, partitions: OrderedDict = None, soft:bool=True ) -> str:
        partition_stmt:str = ''
        if partitions is not None:
            partition_sfield = ','.join([f'{field} {dtype}' for field, dtype in zip(partitions.keys(), partitions.values())])
            partition_stmt = f' PARTITIONED BY ({partition_sfield}) '

        ifn_exist_stmt = ''
        if soft:
            ifn_exist_stmt = 'IF NOT EXISTS'

        sfields = ','.join([f'{field} {dtype} ' for field, dtype in zip(fields.keys(), fields.values())])
        return f'''CREATE TABLE {ifn_exist_stmt} {table_name} ({sfields}) {partition_stmt} STORED AS PARQUET TBLPROPERTIES('compression'='snappy')'''
    @classmethod
    def drop_table_statement(cls, table_name: str) -> str:
        return f'DROP TABLE {table_name}'


        