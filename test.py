from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.python import BranchPythonOperator  
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import pytz 
import logging

local_timezone = pytz.timezone('Asia/Kolkata')

def file_creation_development(**kwargs):
   # environment_type = kwargs['ti'].xcom_pull(task_ids='process_data', key='environment_type')
   environment_type=  kwargs[next(iter(kwargs))]
   logging.info(f"process_data environment_type_recieved: {environment_type}")
   if environment_type == 'development':
        # Write content to a file
        timestamp_str = datetime.now(local_timezone).strftime("%Y-%m-%d_%H-%M-%S")
        with open(f"civalue_development_{timestamp_str}.txt", "w") as file:
            file.write("hello ciValue from development branch")
        print_to_console("development")



def file_creation_production(**kwargs):
    #environment_type = kwargs['ti'].xcom_pull(task_ids='process_data', key='environment_type')
    environment_type=  kwargs[next(iter(kwargs))]
    if environment_type == 'production':
        # Write content to a file
        timestamp_str = datetime.now(local_timezone).strftime("%Y-%m-%d_%H-%M-%S")
        with open(f"civalue_development_{timestamp_str}.txt", "w") as file:
            file.write("hello ciValue from production branch")
        print_to_console("development")


def process_data(**kwargs):
    #environment_type_recieved = kwargs['dag_run'].conf.get('environment_type')       # XComs allow tasks to exchange small amounts of metadata
    #kwargs['ti'].xcom_push(key='environment_type', value=environment_type_recieved) #cross-communication mechanism in Airflow
    #environment_type = kwargs['ti'].xcom_pull(task_ids='process_data', key='environment_type')
   logging.info("process_data environment_type_recieved: ")
   if kwargs:
    environment_type=  kwargs[next(iter(kwargs))]
    if environment_type == 'development':
      file_creation_development(environment_type="development")
    elif environment_type == 'production':
        file_creation_production(environment_type="production")
    else:
        raise ValueError(f"Invalid environment_type: {environment_type}. Allowed values are 'development' or 'production'.")
    


def print_to_console(env):
    print(f"hello ciValue from {env} branch")


process_data(environment_type = "production")