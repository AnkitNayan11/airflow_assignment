# from airflow import DAG
# from airflow.operators.python_operator import PythonOperator
# from airflow.operators.bash_operator import BashOperator
# from datetime import datetime, timedelta

# default_args = {
#     "owner": "Mock_Project",
#     "start_date": datetime(2022, 12, 15),
#     "retries": 1,
#     "retry_delay": timedelta(minutes=5)
# }

# with DAG("MockProject", default_args=default_args, schedule_interval='@daily', catchup=False) as dag:

#     welcome = BashOperator(task_id="WelCome", bash_command="echo Hi, Here We are fetching and publishing Twitter data to "
#                                                            "Kafka Server")

#     # task = PythonOperator(task_id='Publishing_Data_to_Kafka_Server', python_callable=get_twitter_data_for_query1)

#     welcome