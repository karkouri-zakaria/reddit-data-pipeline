from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime, timedelta
import subprocess
import sys
sys.path.append('/opt/airflow/scripts')
from tf_branch import tensorflow_branch
from dbt_branch import dbt_branch
from airflow.operators.bash import BashOperator


def check_s3_for_files(**kwargs):
    s3_hook = S3Hook(aws_conn_id='awsID')
    bucket_name = 'rabbitmq-reddit'
    keys = s3_hook.list_keys(bucket_name=bucket_name)

    if keys:
        # Push S3 keys to XCom
        kwargs['ti'].xcom_push(key='s3_keys', value=keys)
        return ['run_dbt_script', 'run_tensorflow_script']
    else:
        return 'no_files_found'

def run_dbt_func(**kwargs):
    keys = kwargs['ti'].xcom_pull(task_ids='check_s3_for_files', key='s3_keys')
    if keys:
        dbt_branch(keys)

def run_tensorflow_func(**kwargs):
    keys = kwargs['ti'].xcom_pull(task_ids='check_s3_for_files', key='s3_keys')
    if keys:
        tensorflow_branch(keys)

with DAG(
    dag_id="conditional_s3_branching",
    start_date=datetime.now() - timedelta(days=1),
    schedule="@hourly",
    catchup=False,
) as dag:

    start = EmptyOperator(task_id="start")

    check_files = BranchPythonOperator(
        task_id="check_s3_for_files",
        python_callable=check_s3_for_files,
    )

    no_files_found = EmptyOperator(task_id="no_files_found")

    run_dbt_task = PythonOperator(
        task_id='run_dbt_script',
        python_callable=run_dbt_func,
        dag=dag
    )

    run_tensorflow_task = PythonOperator(
        task_id='run_tensorflow_script',
        python_callable=run_tensorflow_func,
        dag=dag
    )

    dbt_run_and_test = BashOperator(
        task_id='dbt_run_and_test',
        bash_command='cd /opt/airflow/scripts/reddit && dbt run && dbt test',
        dag=dag
    )

    join = EmptyOperator(task_id="join", trigger_rule="none_failed_min_one_success")

    # DAG Flow
    start >> check_files
    check_files >> [run_dbt_task, run_tensorflow_task, no_files_found]
    run_dbt_task >> dbt_run_and_test >> join
    run_tensorflow_task >> join
    no_files_found >> join
    
