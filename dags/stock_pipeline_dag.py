from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="stock_pipeline_dag",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    fetch_prices = BashOperator(
        task_id="fetch_prices",
        bash_command="python /opt/airflow/dags/../ingestion/fetch_prices.py"
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/airflow/dags/../dbt_project && dbt run"
    )

    fetch_prices >> dbt_run