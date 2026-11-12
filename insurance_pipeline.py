from datetime import datetime, timedelta
from pathlib import Path

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator

BASE = Path("/home/nazar/insurance-airflow")
PROJECT = BASE / "project"
DBT = PROJECT / "insurance_dbt"
PYTHON = BASE / "venv/bin/python"
DBT_BIN = BASE / "venv/bin/dbt"

with DAG(
    dag_id="insurance_elt_pipeline",
    description="Insurance company ELT pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={
        "owner": "nazar",
        "retries": 1,
        "retry_delay": timedelta(minutes=1),
    },
) as dag:

    extract_load_task = BashOperator(
        task_id="extract_and_load_raw_data",
        bash_command=(
            f'cd "{PROJECT}" && '
            f'"{PYTHON}" data_generator.py && '
            f'"{PYTHON}" load_to_dwh.py'
        ),
    )

    dbt_run_task = BashOperator(
        task_id="dbt_run_transformations",
        bash_command=(
            f'"{DBT_BIN}" run '
            f'--project-dir "{DBT}" '
            f'--profiles-dir "/home/nazar/.dbt"'
        ),
    )

    dbt_test_task = BashOperator(
        task_id="dbt_test",
        bash_command=(
            f'"{DBT_BIN}" test '
            f'--project-dir "{DBT}" '
            f'--profiles-dir "/home/nazar/.dbt"'
        ),
    )

    extract_load_task >> dbt_run_task >> dbt_test_task
