# OVO Test Kit

## installation
create installer : 

```
    python3 setup.py sdist bdist_wheel
```

installer will be at ```dist/``` directory
install using : 
```
pip3 install dist/<generated-file>.whl
```

## Quickstart

```python
from ovobdkit.testkit import OVOTestKit
import unittest
class TestMlmMerchant(OVOTestKit):
    TABLE_NAME = 'ovo_raw.ovo_smp_mlm_merchant'
    FIELDS = '''
        id BigInt
        merchant_code String
        grab_id String
    '''
    def test_having_no_duplicates(self):
        self.duplicate_check(TestMlmMerchant.TABLE_NAME)


if __name__ == '__main__':
    unittest.main()
```
more? see examples directories 

## Functionalities
- Unit Test
- Functional Test
    - Communicate to Airflow
    - Communicate to OMT

# Common case
- get all (example / merchant_owner)
- delta (example / springreward/txn_ledger)
- delta with update (example/springreward/customer_transaction)