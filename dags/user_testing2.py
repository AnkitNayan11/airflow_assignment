# from airflow import DAG
# from datetime import datetime
# from datetime import datetime, timedelta
# from airflow.operators.postgres_operator import PostgresOperator
# from airflow.operators.bash_operator import BashOperator

# # from airflow.providers.http.sensors.http import HttpSensor
# # from airflow.providers.http.operators.http import SimpleHttpOperator
# # import json

# default_args = {
#     "owner": "Mock_Project",
#     "start_date": datetime(2022, 12, 15),
#     "retries": 5,
#     "retry_delay": timedelta(minutes=5)
# }

# with DAG(dag_id='user_processing',  schedule_interval='@daily', default_args=default_args, catchup=False) as dag:
#     welcome = BashOperator(task_id="WelCome_Ankit", bash_command="echo Hi, Here We are creating table")

#     create_table = PostgresOperator(
#         task_id='create_table',
#         postgres_conn_id='postgres',
#         sql='''
#             CREATE TABLE IF NOT EXISTS users (
#                 firstname TEXT NOT NULL,
#                 lastname TEXT NOT NULL,
#                 country TEXT NOT NULL,
#                 username TEXT NOT NULL,
#                 password TEXT NOT NULL,
#                 email TEXT NOT NULL
#             );
#         '''
#     )
