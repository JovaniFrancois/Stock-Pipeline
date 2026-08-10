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
        bash_command="python /opt/airflow/ingestion/fetch_prices.py",
        env={"DB_HOST": "host.docker.internal"}
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/airflow/dbt_project && echo DB_HOST_IS: $DB_HOST && /home/airflow/.local/bin/dbt run --no-partial-parse",
        env={"DB_HOST": "host.docker.internal"}
    )

    fetch_prices >> dbt_run