import json
import os
import pandas as pd

from datasources.graphql_ahr import GraphQlAHRData
from pandas._testing import assert_frame_equal
from test_utils import _load_df_from_bigquery
from unittest import mock

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = os.path.join(THIS_DIR, os.pardir, "data", "graphql_ahr")
GOLDEN_DIR = os.path.join(TEST_DIR, "golden_data")

TEST_FILE = os.path.join(TEST_DIR, 'response_data.json')

GOLDEN_DATA = {
    'age_national': os.path.join(GOLDEN_DIR, 'age_national.csv'),
    'sex_national': os.path.join(GOLDEN_DIR, "sex_national.csv"),
    'race_and_ethnicity_state': os.path.join(GOLDEN_DIR, 'race_and_ethnicity_state.csv'),
}


def _fetch_ahr_data_from_graphql():
    with open(TEST_FILE, 'r') as file:
        data = json.load(file)

    return data


@mock.patch('ingestion.gcs_to_bq_util.add_df_to_bq', return_value=None)
@mock.patch('ingestion.gcs_to_bq_util.fetch_ahr_data_from_graphql', side_effect=_fetch_ahr_data_from_graphql)
@mock.patch('ingestion.gcs_to_bq_util.load_df_from_bigquery', side_effect=_load_df_from_bigquery)
def testWriteToBqAgeNational(mock_pop: mock.MagicMock, mock_fetch: mock.MagicMock, mock_bq: mock.MagicMock):
    datasource = GraphQlAHRData()
    datasource.write_to_bq('dataset', 'gcs_bucket', demographic='age', geographic='national')

    actual_df, _, table_name = mock_bq.call_args_list[0][0]
    expected_df = pd.read_csv(GOLDEN_DATA[table_name], dtype={"state_fips": str})
    assert table_name == "age_national"

    assert mock_bq.call_count == 1

    assert_frame_equal(actual_df, expected_df, check_like=True)


@mock.patch('ingestion.gcs_to_bq_util.add_df_to_bq', return_value=None)
@mock.patch('ingestion.gcs_to_bq_util.fetch_ahr_data_from_graphql', side_effect=_fetch_ahr_data_from_graphql)
@mock.patch('ingestion.gcs_to_bq_util.load_df_from_bigquery', side_effect=_load_df_from_bigquery)
def testWriteToBqRaceNational(mock_pop: mock.MagicMock, mock_fetch: mock.MagicMock, mock_bq: mock.MagicMock):
    datasource = GraphQlAHRData()
    datasource.write_to_bq('dataset', 'gcs_bucket', demographic='race_and_ethnicity', geographic='state')

    actual_df, _, table_name = mock_bq.call_args_list[0][0]
    expected_df = pd.read_csv(GOLDEN_DATA[table_name], dtype={"state_fips": str})
    assert table_name == "race_and_ethnicity_state"

    assert mock_bq.call_count == 1

    assert_frame_equal(actual_df, expected_df, check_like=True)


@mock.patch('ingestion.gcs_to_bq_util.add_df_to_bq', return_value=None)
@mock.patch('ingestion.gcs_to_bq_util.fetch_ahr_data_from_graphql', side_effect=_fetch_ahr_data_from_graphql)
@mock.patch('ingestion.gcs_to_bq_util.load_df_from_bigquery', side_effect=_load_df_from_bigquery)
def testWriteToBqSexNational(mock_pop: mock.MagicMock, mock_fetch: mock.MagicMock, mock_bq: mock.MagicMock):
    datasource = GraphQlAHRData()
    datasource.write_to_bq('dataset', 'gcs_bucket', demographic='sex', geographic='national')

    actual_df, _, table_name = mock_bq.call_args_list[0][0]
    expected_df = pd.read_csv(GOLDEN_DATA[table_name], dtype={"state_fips": str})

    assert table_name == "sex_national"
    assert mock_bq.call_count == 1

    assert_frame_equal(actual_df, expected_df, check_like=True)