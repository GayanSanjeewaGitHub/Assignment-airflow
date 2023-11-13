from airflow.operators.python_operator import PythonOperator

def trigger_workflow(**kwargs):
    # Simulate API request
    environment_type = "development"  # Replace with your dynamic value
    kwargs['ti'].xcom_push(key='environment_type', value=environment_type)

api_trigger_task = PythonOperator(
    task_id='api_trigger',
    python_callable=trigger_workflow,
    provide_context=True,
    dag=dag,
)
