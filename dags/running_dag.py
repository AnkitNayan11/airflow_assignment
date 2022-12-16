from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from airflow.operators.dummy_operator import DummyOperator
from airflow import DAG
from airflow.models import TaskInstance
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime,timedelta
from airflow.models import DagRun
from airflow.models import Variable

#from connect_with_snowflake import *

default_args = {
    "owner": "assignment",
    "start_date": datetime(2022, 12, 16),
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

def get_task_status(dag_id, task_id):
    """ Returns the status of the last dag run for the given dag_id

    Args:
        dag_id (str): The dag_id to check
        task_id (str): The task_id to check
    Returns:
        List - The status of the last dag run for the given dag_id
    """
    last_dag_run = DagRun.find(dag_id=dag_id)
    last_dag_run.sort(key=lambda x: x.execution_date, reverse=True)
    return last_dag_run[0].get_task_instance(task_id).state

#list = ["WelCome", ]

with DAG("assignment", default_args=default_args, schedule_interval='@daily', catchup=False) as dag:

    welcome = BashOperator(task_id="WelCome", bash_command="echo Hi, Running the tasks")

    #dag1 = PythonOperator(task_id='reading data from snowflake', python_callable=connect_with_snowflake)

    dag2_create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres',
        sql='''
            CREATE TABLE IF NOT EXISTS pet (
            name VARCHAR NOT NULL,
            pet_type VARCHAR NOT NULL,
            birth_date DATE NOT NULL,
            OWNER VARCHAR NOT NULL
            );
        '''
    )

    dag3_insert_data = PostgresOperator(
        task_id='insert_data',
        postgres_conn_id='postgres',
        sql='''
            INSERT INTO pet VALUES ( 'Max', 'Dog', '2018-07-05', 'Jane');
            INSERT INTO pet VALUES ( 'Susie', 'Cat', '2019-05-01', 'Phil');
            INSERT INTO pet VALUES ( 'Lester', 'Hamster', '2020-06-23', 'Lily');
            INSERT INTO pet VALUES ( 'Quincy', 'Parrot', '2013-08-11', 'Anne');
        '''
    )

    dag4_fetch_data = PostgresOperator(
        task_id='fetch_data',
        postgres_conn_id='postgres',
        sql='''
            select * from pet;
        '''
    )

    # t3 = PythonOperator(
    #         task_id = 'get_task_status',
    #         python_callable = get_task_status,
    #         op_args = ['assignment', 'WelCome'],
    #         do_xcom_push = False
    #     )

    trigger_dependent_dag = TriggerDagRunOperator(
        task_id="show_dag1_status",
        trigger_dag_id="assignment_dag_status",
        trigger_rule="all_done"
        )
       
welcome>>dag2_create_table>>dag3_insert_data>>dag4_fetch_data>>trigger_dependent_dag

with DAG(dag_id="assignment_dag_status", start_date=datetime(2022,12,16), schedule_interval="@daily",max_active_runs=1, catchup=False) as dag:
        show_dag1_status = PythonOperator(
        task_id="show_dag1_status",
        python_callable=get_task_status,
        op_args = ['assignment', 'dag4_fetch_data'],
        do_xcom_push = False)


