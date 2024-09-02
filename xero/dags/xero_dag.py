from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import sys
import os

# Add the code directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'code'))

from pipeline import run_pipeline
from config import CONFIG

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'xero_data_pipeline',
    default_args=default_args,
    description='A DAG to run the Xero data pipeline',
    schedule_interval=timedelta(days=1),
    catchup=False,
)

def run_xero_pipeline(**context):
    # Allow overriding client name when triggering DAG run
    client_name = context['dag_run'].conf.get('client_name', CONFIG['CLIENT_NAME'])
    bucket_name = f"{CONFIG['PROJECT_ID']}-{client_name}-xero-data"
    run_pipeline(bucket_name)

run_pipeline_task = PythonOperator(
    task_id='run_xero_pipeline',
    python_callable=run_xero_pipeline,
    provide_context=True,
    dag=dag,
)

run_pipeline_task