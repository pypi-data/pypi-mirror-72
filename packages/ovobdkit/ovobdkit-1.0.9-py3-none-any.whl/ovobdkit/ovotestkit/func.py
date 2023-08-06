from datetime import datetime
from bash import bash
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func as sql_function
import pandas as pd
from pprint import pprint

import imaplib
import smtplib
import email

class AirflowClient :
    def __init__(self,usr='airflow',pwd='airflow',host='10.30.225.172',port='5432',dbname='airflow-dev', airflow_bin='/home/airflow/venv/bin/airflow'):
        self.engine = db.create_engine(f'postgresql+psycopg2://{usr}:{pwd}@{host}:{port}/{dbname}')
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()
        Session = sessionmaker()
        Session.configure(bind=self.engine)

        self.session = Session()


        self.airflow = airflow_bin

    def get_variable(self, key:str):
        V = db.Table('variable', self.metadata, autoload=True, autoload_with=self.engine)
        return self.session.query(V).filter(V.columns.key == key).first()

    def dag_status(self, dag_id, prc_dt=datetime.now().strftime('%Y%m%d')):
        dag = db.Table('dag_run',self.metadata, autoload=True, autoload_with=self.engine)
        print(f'{prc_dt} 00:00:00')
        dt_start = datetime.strptime(f'{prc_dt} 00:00:00','%Y%m%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        dt_end = datetime.strptime(f'{prc_dt} 23:59:59','%Y%m%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

        print('start',dt_start, 'end', dt_end)
        res = self.session.query(dag).filter(dag.columns.dag_id == dag_id)\
                .filter(dag.columns.execution_date >= dt_start )\
                .filter(dag.columns.execution_date <= dt_end )\
                .all() #.filter(dag.columns.execution_date == datetime.strptime(prc_dt , '%Y%m%d').strftime('%Y-%m-%d'))
        
        df = pd.DataFrame(res)
        return df['state'].values[0]

    def run_or_clear_dag(self,dag_id,prc_dt):
        exec_date = datetime.strptime(prc_dt, '%Y%m%d').strftime('%Y-%m-%d')
        run_cmd = f'''   
            {self.airflow} trigger_dag -e {exec_date} {dag_id}

            if [[ $? -ne 0 ]]; then
                {self.airflow} clear -s {exec_date} -e {exec_date} -c {dag_id}
            fi
        '''
        bash(run_cmd)
OMT_RUNNING =  'RUNNING'
OMT_SUCCESS =  'SUCCESS'

class OMTClient:
    
    OMT_RUNNING =  'RUNNING'
    OMT_SUCCESS =  'SUCCESS'

    def __init__(self,mail_login=None, mail_password=None):
        self.login = mail_login
        self.password = mail_password

    def create_db_session(self, dbname, usr='omt', pwd='omt', host='10.30.225.239', port='5432'):
        dbschema = 'dev'
        self.engine = db.create_engine(f'postgresql+psycopg2://{usr}:{pwd}@{host}:{port}/{dbname}') #,
            #connect_args={'options': '-csearch_path={}'.format(dbschema)})
        self.connection = self.engine.connect()
        self.metadata = db.MetaData(schema='dev')
        Session = sessionmaker()
        Session.configure(bind=self.engine)

        self.session = Session()
        return self.session


    
    def get_entry(self,
            job_id:str=None, 
            key:str=None, 
            target_tbl:str=None, 
            prc_dt:str = None,
            status:str=OMT_SUCCESS , 
            is_dev:bool=True
        ):
        # print("status : ", status)
        if status != OMT_RUNNING and status != OMT_SUCCESS:
            raise Exception("UNKNOWN job status, pass OMTClient.OMT_RUNNING or OMTClient.OMT_SUCCESS")

        # schema = 'prd'
        # if is_dev:
        #     schema = 'dev'

        _ = self.create_db_session(dbname='omt')
        omt = db.Table(f'omt', self.metadata, autoload=True, autoload_with=self.engine)

        # print(self.session.query(omt).first())

        sess = self.session.query(omt).filter(omt.columns.job_status == status)

        if key is not None:
            sess = sess.filter(omt.columns.key_id==key)

        if job_id is not None:
            sess = sess.filter(omt.columns.job_id==job_id)
        else :
            max_job_id = self.session.query(
                            sql_function.max(omt.columns.job_id)
                        ).filter(omt.columns.target_tbl==target_tbl).scalar()
            print("max job id ", max_job_id)
            sess = sess.filter(omt.columns.job_id==max_job_id)

        if target_tbl is not None:
            sess = sess.filter(omt.columns.target_tbl == target_tbl)
        
        if prc_dt is not None:
            sess = sess.filter(omt.columns.date_grp == prc_dt)

        return sess.first()

    def omt_run_exists_in_slack(self, omt_signature, job_id):
        raise NotImplementedError()


    def omt_success_exists_in_email(self, omt_signature, prc_dt, omt_sender='bigdata.support@ovo.id'):
        print("login mail")
        mail=imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(self.login,self.password)
        mail.select(mailbox='INBOX')
        # SUCCESS 20200423
        #
        typ,data=mail.search(None,f'(FROM "{omt_sender}" SUBJECT "[SUCCESS] {omt_signature} - RAW, process Date: {prc_dt}")')
        print("get response")
        # pprint(data)

        for num in data[0].split():
            typ, data = mail.fetch(num, '(RFC822)')
            for response_part in data :
                
                if isinstance(response_part,tuple):
                    
                    msg=email.message_from_string(response_part[1].decode('utf-8'))
                    # print(msg)
                    print ("subj:", msg['subject'])
                    print ("from:", msg['from'])
                    print ("body:")

                    return True
                    
        mail.close()
        mail.logout()


def main():
    # airflow = AirflowClient()
    # airflow.run_dag(dag_id='ovo_smp_db_daily_pten_regist',prc_dt='20200420')
    # res = airflow.dag_status(dag_id='ovo_smp_db_daily_pten_regist', prc_dt='20200415')
    # print(res)
 
    omt = OMTClient()
    stat = omt.omt_success_exists_in_email(omt_signature='OVO_SMP_MLM_MERCHANT',prc_dt='20200302')
    print(f"IS SUCCESS {stat}")

if __name__ == "__main__":
    main()