# TODO: Rename our airflow/ as it tries to import from that and not the pip airflow
# pylint: disable=no-name-in-module
from airflow import DAG  # type: ignore
from airflow.utils.dates import days_ago  # type: ignore
from datetime import timedelta
import util

_BJS_INCARCERATION_WORKFLOW_ID = "BJS_INCARCERATION_DATA"
_BJS_INCARCERATION_DATASET_NAME = "bjs_incarceration_data"

default_args = {
    "start_date": days_ago(0),
    "execution_timeout": timedelta(minutes=15),
}

data_ingestion_dag = DAG(
    "bjs_incarceration_ingestion_dag",
    default_args=default_args,
    schedule_interval=None,
    description="Ingestion configuration for BJS",
)

bjs_incarceration_bq_payload = util.generate_bq_payload(_BJS_INCARCERATION_WORKFLOW_ID, _BJS_INCARCERATION_DATASET_NAME)
bjs_incarceration_bq_operator = util.create_bq_ingest_operator(
    "bjs_incarceration_to_bq", bjs_incarceration_bq_payload, data_ingestion_dag
)

payload_race = {
    "dataset_name": _BJS_INCARCERATION_DATASET_NAME,
    "should_export_as_alls": True,
    "demographic": "race_and_ethnicity",
}
bjs_incarceration_exporter_operator_race = util.create_exporter_operator(
    "bjs_incarceration_exporter_race", payload_race, data_ingestion_dag
)

payload_age = {"dataset_name": _BJS_INCARCERATION_DATASET_NAME, "demographic": "age"}
bjs_incarceration_exporter_operator_age = util.create_exporter_operator(
    "bjs_incarceration_exporter_age", payload_age, data_ingestion_dag
)


payload_sex = {"dataset_name": _BJS_INCARCERATION_DATASET_NAME, "demographic": "sex"}
bjs_incarceration_exporter_operator_sex = util.create_exporter_operator(
    "bjs_incarceration_exporter_sex", payload_sex, data_ingestion_dag
)

# Ingestion DAG
(
    bjs_incarceration_bq_operator
    >> [
        bjs_incarceration_exporter_operator_race,
        bjs_incarceration_exporter_operator_age,
        bjs_incarceration_exporter_operator_sex,
    ]
)
