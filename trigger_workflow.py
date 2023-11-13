from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.python import BranchPythonOperator  
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import pytz 

local_timezone = pytz.timezone('Asia/Kolkata')

default_args = {
    'owner': 'airflow',
    'depends_on_past': False, #not considering success of previous execution of DAG
    'start_date': local_timezone.localize(datetime.now()) + timedelta(seconds=2),
    'retries': 0,
    'email_on_failure' : False,  # if need to add  the email change the  file airflow.cfg
    'email_on_retry' : False  
}

dag = DAG(
    'my_workflow3',  #id
    default_args=default_args,
    schedule_interval= timedelta(seconds=20), # re run two times just for test puprpose after 20s
    max_active_runs= 2 
)

def trigger_workflow(**kwargs):
    environment_type = "development"                                       # XComs allow tasks to exchange small amounts of metadata
    kwargs['ti'].xcom_push(key='environment_type', value=environment_type) #cross-communication mechanism in Airflow

# api_trigger_task = PythonOperator(
#     task_id='api_trigger',                                   #unique identifier for the task
#     python_callable=trigger_workflow,         
#     provide_context=True,                                    # access to this context 
#     dag=dag,
# )

def file_creation_development(**kwargs):
    environment_type = kwargs['ti'].xcom_pull(task_ids='process_data', key='environment_type')
    if environment_type == 'development':
        # Write content to a file
        with open(f"civalue_development_{datetime.now()}.txt", "w") as file:
            file.write("hello ciValue from development branch")
        print_to_console("development")

file_creation_development = PythonOperator(
    task_id='file_creation_development',
    python_callable=file_creation_development,
    provide_context=True,
    dag=dag,
)

def file_creation_production(**kwargs):
    environment_type = kwargs['ti'].xcom_pull(task_ids='process_data', key='environment_type')
    if environment_type == 'production':
        # Write content to a file
        with open(f"civalue_production_{datetime.now()}.txt", "w") as file:
            file.write("hello ciValue from production branch")
        print_to_console("production")


file_creation_production = PythonOperator(
    task_id='file_creation_production',
    python_callable=file_creation_production,
    provide_context=True,
    dag=dag,
)

def process_data(**kwargs):
    environment_type_test_value = "development"                                       # XComs allow tasks to exchange small amounts of metadata
    kwargs['ti'].xcom_push(key='environment_type', value=environment_type_test_value) #cross-communication mechanism in Airflow
    environment_type = kwargs['ti'].xcom_pull(task_ids='process_data', key='environment_type')
    if environment_type == 'development':
        return 'file_creation_development'
    elif environment_type == 'production':
        return 'file_creation_production'
    else:
        raise ValueError(f"Invalid environment_type: {environment_type}. Allowed values are 'development' or 'production'.")


process_data = BranchPythonOperator(
    task_id='process_data',
    python_callable=process_data,
    provide_context=True,
    dag=dag,
)


def print_to_console(env):
    print(f"hello ciValue from {env} branch")

print_to_console = BranchPythonOperator(
    task_id='print_to_console',
    python_callable=print_to_console,
    provide_context=True,
    dag=dag,
)



process_data >> [file_creation_development , file_creation_production]
file_creation_development >> [print_to_console]
file_creation_production >> [print_to_console]
