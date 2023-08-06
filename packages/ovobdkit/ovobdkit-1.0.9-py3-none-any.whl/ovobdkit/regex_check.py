
import re

ctab_stmt = '''
CREATE TABLE ovo_gold.ovo_spring_activity_report (
  txndate STRING,
  source_used_id STRING,
  customer_identification_no STRING,
  account_reference_no STRING,
  account_number STRING,
  txn_number STRING,
  partner_ref_txn_id STRING,
  txn_category STRING,
  txn_amount DECIMAL(38,3),
  partner_message_id STRING,
  partner_txn_id STRING,
  partner_txn_type STRING,
  ppn_dttm TIMESTAMP,
  prc_dt STRING,
  job_id STRING
)
PARTITIONED BY (
  date_partition STRING
)
WITH SERDEPROPERTIES ('serialization.format'='1')
STORED AS PARQUET
LOCATION 'hdfs://ovodevbd/user/hive/warehouse/ovo_gold.db/ovo_spring_activity_report'
TBLPROPERTIES ('parquet.compression'='SNAPPY', 'spark.sql.sources.schema.numPartCols'='1', 'spark.sql.sources.schema.numParts'='1', 'spark.sql.sources.schema.part.0'='{\"type\":\"struct\",\"fields\":[{\"name\":\"txndate\",\"type\":\"string\",\"nullable\":true,\"metadata\":{\"HIVE_TYPE_STRING\":\"string\"}},{\"name\":\"source_used_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{\"HIVE_TYPE_STRING\":\"string\"}},{\"name\":\"customer_identification_no\",\"type\":\"string\",\"nullable\":true,\"metadata\":{\"HIVE_TYPE_STRING\":\"string\"}},{\"name\":\"account_reference_no\",\"type\":\"string\",\"nullable\":true,\"metadata\":{\"HIVE_TYPE_STRING\":\"string\"}},{\"name\":\"account_number\",\"type\":\"string\",\"nullable\":true,\"metadata\":{\"HIVE_TYPE_STRING\":\"string\"}},{\"name\":\"txn_number\",\"type\":\"string\",\"nullable\":true,\"metadata\":{\"HIVE_TYPE_STRING\":\"string\"}},{\"name\":\"partner_ref_txn_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{\"HIVE_TYPE_STRING\":\"string\"}},{\"name\":\"txn_category\",\"type\":\"string\",\"nullable\":true,\"metadata\":{\"HIVE_TYPE_STRING\":\"string\"}},{\"name\":\"txn_amount\",\"type\":\"decimal(38,3)\",\"nullable\":true,\"metadata\":{\"HIVE_TYPE_STRING\":\"decimal(38,3)\"}},{\"name\":\"partner_message_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{\"HIVE_TYPE_STRING\":\"string\"}},{\"name\":\"partner_txn_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{\"HIVE_TYPE_STRING\":\"string\"}},{\"name\":\"partner_txn_type\",\"type\":\"string\",\"nullable\":true,\"metadata\":{\"HIVE_TYPE_STRING\":\"string\"}},{\"name\":\"ppn_dttm\",\"type\":\"timestamp\",\"nullable\":true,\"metadata\":{\"HIVE_TYPE_STRING\":\"timestamp\"}},{\"name\":\"prc_dt\",\"type\":\"string\",\"nullable\":true,\"metadata\":{\"HIVE_TYPE_STRING\":\"string\"}},{\"name\":\"job_id\",\"type\":\"string\",\"nullable\":true,\"metadata\":{\"HIVE_TYPE_STRING\":\"string\"}},{\"name\":\"date_partition\",\"type\":\"string\",\"nullable\":true,\"metadata\":{\"HIVE_TYPE_STRING\":\"string\"}}]}', 'spark.sql.sources.schema.partCol.0'='date_partition')
'''

def test_find_parquet():
    
    p = re.compile(r'(stored as parquet)')
    r = p.findall(ctab_stmt.lower())
    print(r)

def test_find_snappy():
    
    p = re.compile(r"('parquet.compression'='snappy')")
    r = p.findall(ctab_stmt.lower())
    print(r)

if __name__ == "__main__":
    test_find_parquet()
    test_find_snappy()