from datetime import datetime
from bash import bash
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
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

    def run_dag(self,dag_id, prc_dt):
        exec_date = datetime.strptime(prc_dt, '%Y%m%d').strftime('%Y-%m-%d')
        run_cmd = f'''   
            {self.airflow} trigger_dag -e {exec_date} {dag_id}

            if [[ $? -ne 0 ]]; then
                {self.airflow} clear -s {exec_date} -e {exec_date} -c {dag_id}
            fi
        '''
        bash(run_cmd)

class OMTClient:
    
    def __init__(self,login, password):
        self.login = login
        self.password = password

    def is_success(self, omt_signature, prc_dt):
        print("login mail")
        mail=imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(self.login,self.password)
        mail.select(mailbox='INBOX')
        # SUCCESS 20200423
        #
        typ,data=mail.search(None,f'(FROM "bigdata.support@ovo.id" SUBJECT "[SUCCESS] {omt_signature} - RAW, process Date: {prc_dt}")')
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
    stat = omt.is_success(omt_signature='OVO_SMP_MLM_MERCHANT',prc_dt='20200302')
    print(f"IS SUCCESS {stat}")

if __name__ == "__main__":
    main()