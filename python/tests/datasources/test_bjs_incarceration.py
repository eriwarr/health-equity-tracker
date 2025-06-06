# pylint: disable=no-member
# NOTE: pylint not treating output from read_json as a df, despite trying chunksize None

from unittest import mock
import os
from io import StringIO
import pandas as pd
from pandas._testing import assert_frame_equal
from datasources.bjs_incarceration import BJSIncarcerationData
from ingestion.bjs_utils import (
    strip_footnote_refs_from_df,
    missing_data_to_nan,
    set_state_col,
)


# INTEGRATION TEST SETUP


def _get_test_table_files(*args):
    [zip_url, table_crops] = args
    print("URL (mock) requested:", zip_url)

    loaded_tables = {}
    for file in table_crops.keys():
        if file in table_crops:
            source_df = pd.read_csv(
                os.path.join(TEST_DIR, f"bjs_test_input_{file}"),
                encoding="ISO-8859-1",
                thousands=",",
                engine="python",
            )

            source_df = strip_footnote_refs_from_df(source_df)
            source_df = missing_data_to_nan(source_df)
            loaded_tables[file] = set_state_col(source_df)

    return loaded_tables


def _get_prison_2():
    """generate a df that matches the cleaned and standardized BJS table
    needed for generate_breakdown_df()"""
    table_2_data = StringIO(
        """All,Male,Female,state_name
1215821.0,1132767.0,83054.0,U.S. total
25328.0,23166.0,2162.0,Alabama"""
    )
    df_2 = pd.read_csv(table_2_data, sep=",")
    return df_2


def _get_prison_10():
    """generate a df that matches the cleaned and standardized BJS table
    needed for generate_breakdown_df()"""
    table_10_data = StringIO(
        """age,prison_pct_share,state_name
All,100.0,United States
18-19,0.6,United States
20-24,7.5,United States
25-29,14.5,United States
30-34,16.3,United States
35-39,15.8,United States
40-44,13.0,United States
45-49,10.1,United States
50-54,8.1,United States
55-59,6.5,United States
60-64,4.0,United States
65+,3.5,United States
Number of sentenced prisoners,1182166.0,United States"""
    )
    df_10 = pd.read_csv(table_10_data, sep=",")
    return df_10


def _get_prison_13():
    """generate a df that matches the cleaned and standardized BJS table
    needed for generate_breakdown_df()"""
    table_13_data = StringIO(
        """state_name,prison_estimated_total,age
United States,352,0-17
Alabama,1,0-17
    """
    )
    df_13 = pd.read_csv(table_13_data, sep=",")
    return df_13


def _get_prison_23():
    """generate a df that matches the cleaned and standardized BJS table
    needed for generate_breakdown_df()"""
    table_23_data = StringIO(
        """ALL,state_name
196.0,American Samoa"""
    )
    df_23 = pd.read_csv(table_23_data, sep=",")
    return df_23


def _get_prison_app2():
    header_line = "ALL,WHITE_NH,BLACK_NH,HISP,AIAN_NH,ASIAN_NH,NHPI_NH,MULTI_NH,OTHER_STANDARD_NH,UNKNOWN,state_name"
    table_app_2_data = StringIO(
        f"""{header_line}
152156.0,44852.0,55391.0,46162.0,3488.0,2262.0,,,0.0,1.0,Federal
,,,,,,,,,,State
25328.0,11607.0,13519.0,0.0,2.0,3.0,0.0,0.0,0.0,197.0,Alabama"""
    )
    df_app_2 = pd.read_csv(table_app_2_data, sep=",")
    return df_app_2


def _get_jail_6():
    header_line = (
        "state_name,jail_estimated_total,0-17,18+,Male 0-17,Male 18+,Female 0-17,Female 18+,Male Pct,Female Pct"
    )

    table_6_data = StringIO(
        f"""{header_line}
United States,734470,2880,731580,2660,621070,230,110510,84.9,15.1
Alabama,16450,34,16410,34,13680,0,2730,83.4,16.6"""
    )
    df_6 = pd.read_csv(table_6_data, sep=",")

    return df_6


def _get_jail_7():
    table_7_data = StringIO(
        """ALL,WHITE_NH,BLACK_NH,HISP,AIAN_NH,ASIAN_NH,NHPI_NH,MULTI_NH,state_name
734470.0,49.4,33.6,14.6,1.4,0.6,0.1,0.3,United States
386770.0,49.7,40.0,9.3,0.5,0.3,,0.1,South
16450.0,53.8,43.2,2.7,0.1,0.1,,,Alabama"""
    )
    df_7 = pd.read_csv(table_7_data, sep=",")
    return df_7


# Current working directory.
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = os.path.join(THIS_DIR, os.pardir, "data", "bjs_incarceration")

GOLDEN_DATA = {
    "race_national": os.path.join(TEST_DIR, "bjs_test_output_race_and_ethnicity_national.json"),
    "age_national": os.path.join(TEST_DIR, "bjs_test_output_age_national.json"),
    "sex_national": os.path.join(TEST_DIR, "bjs_test_output_sex_national.json"),
    "race_state": os.path.join(TEST_DIR, "bjs_test_output_race_and_ethnicity_state.json"),
    "age_state": os.path.join(TEST_DIR, "bjs_test_output_age_state.json"),
    "sex_state": os.path.join(TEST_DIR, "bjs_test_output_sex_state.json"),
}

expected_dtype = {
    "state_name": str,
    "state_fips": str,
    "prison_per_100k": float,
    "prison_pct_share": float,
    "jail_per_100k": float,
    "jail_pct_share": float,
    "confined_children_estimated_total": int,
    "population": object,
    "incarceration_population_pct": float,
}
expected_dtype_age = {
    **expected_dtype,
    "age": str,
    "incarceration_population_estimated_total": float,
}
expected_dtype_race = {
    **expected_dtype,
    "race_and_ethnicity": str,
    "incarceration_population_estimated_total": float,
    "prison_estimated_total": float,
    "jail_estimated_total": float,
}

expected_dtype_sex = {
    **expected_dtype,
    "sex": str,
    "incarceration_population_estimated_total": float,
    "prison_estimated_total": float,
    "jail_estimated_total": float,
}

# --- INTEGRATION TESTS NATIONAL LEVEL


# - AGE
def testGenerateBreakdownAgeNational():
    df_prison_10 = _get_prison_10()
    df_prison_13 = _get_prison_13()
    df_jail_6 = _get_jail_6()

    datasource = BJSIncarcerationData()
    df = datasource.generate_breakdown_df("age", "national", [df_prison_10, df_jail_6], [df_prison_13, df_jail_6])
    expected_df_age_national = pd.read_json(GOLDEN_DATA["age_national"], dtype=expected_dtype_age)

    df = df.sort_values(by=["state_name", "age"]).reset_index(drop=True)
    expected_df_age_national = expected_df_age_national.sort_values(by=["state_name", "age"]).reset_index(drop=True)

    assert_frame_equal(df, expected_df_age_national, check_like=True)


# - RACE
def testGenerateBreakdownRaceNational():
    prison_app_2 = _get_prison_app2()
    prison_23 = _get_prison_23()
    prison_13 = _get_prison_13()
    jail_6 = _get_jail_6()
    jail_7 = _get_jail_7()

    datasource = BJSIncarcerationData()
    df = datasource.generate_breakdown_df(
        "race_and_ethnicity",
        "national",
        [prison_app_2, prison_23, jail_7],
        [prison_13, jail_6],
    )

    expected_df_race_national = pd.read_json(GOLDEN_DATA["race_national"], dtype=expected_dtype_race)
    df = df.sort_values(by=["state_name", "race_and_ethnicity"]).reset_index(drop=True)
    expected_df_race_national = expected_df_race_national.sort_values(
        by=["state_name", "race_and_ethnicity"]
    ).reset_index(drop=True)

    assert_frame_equal(df, expected_df_race_national, check_like=True)


# - SEX


def testGenerateBreakdownSexNational():
    prison_2 = _get_prison_2()
    prison_23 = _get_prison_23()
    prison_13 = _get_prison_13()
    jail_6 = _get_jail_6()

    datasource = BJSIncarcerationData()
    df = datasource.generate_breakdown_df("sex", "national", [prison_2, prison_23, jail_6], [prison_13, jail_6])

    expected_df_sex_national = pd.read_json(GOLDEN_DATA["sex_national"], dtype=expected_dtype_sex)

    df = df.sort_values(by=["state_name", "sex"]).reset_index(drop=True)
    expected_df_sex_national = expected_df_sex_national.sort_values(by=["state_name", "sex"]).reset_index(drop=True)

    assert_frame_equal(df, expected_df_sex_national, check_like=True)


# # INTEGRATION TEST - STATE LEVEL


# - SEX


def testGenerateBreakdownSexState():
    prison_2 = _get_prison_2()
    prison_23 = _get_prison_23()
    prison_13 = _get_prison_13()
    jail_6 = _get_jail_6()

    datasource = BJSIncarcerationData()
    df = datasource.generate_breakdown_df("sex", "state", [prison_2, prison_23, jail_6], [prison_13, jail_6])

    expected_df_sex_state = pd.read_json(GOLDEN_DATA["sex_state"], dtype=expected_dtype_sex)

    df = df.sort_values(by=["state_name", "sex"]).reset_index(drop=True)
    expected_df_sex_state = expected_df_sex_state.sort_values(by=["state_name", "sex"]).reset_index(drop=True)

    assert_frame_equal(df, expected_df_sex_state, check_like=True)


# - AGE
def testGenerateBreakdownAgeState():
    prison_2 = _get_prison_2()
    prison_23 = _get_prison_23()
    prison_13 = _get_prison_13()
    jail_6 = _get_jail_6()

    datasource = BJSIncarcerationData()
    df = datasource.generate_breakdown_df("age", "state", [prison_2, prison_23, jail_6], [prison_13, jail_6])

    expected_df_age_state = pd.read_json(GOLDEN_DATA["age_state"], dtype=expected_dtype_age)

    df = df.sort_values(by=["state_name", "age"]).reset_index(drop=True)
    expected_df_age_state = expected_df_age_state.sort_values(by=["state_name", "age"]).reset_index(drop=True)

    assert_frame_equal(df, expected_df_age_state, check_like=True)


# # - RACE
def testGenerateBreakdownRaceState():
    prison_app_2 = _get_prison_app2()
    prison_23 = _get_prison_23()
    prison_13 = _get_prison_13()
    jail_6 = _get_jail_6()
    jail_7 = _get_jail_7()

    datasource = BJSIncarcerationData()
    df = datasource.generate_breakdown_df(
        "race_and_ethnicity",
        "state",
        [prison_app_2, prison_23, jail_7],
        [prison_13, jail_6],
    )

    expected_df_race_state = pd.read_json(GOLDEN_DATA["race_state"], dtype=expected_dtype_race)

    df = df.sort_values(by=["state_name", "race_and_ethnicity"]).reset_index(drop=True)
    expected_df_race_state = expected_df_race_state.sort_values(by=["state_name", "race_and_ethnicity"]).reset_index(
        drop=True
    )

    assert_frame_equal(df, expected_df_race_state, check_like=True)


# INTEGRATION TEST - CORRECT NETWORK CALLS
# comment out all mocks expect BQ to see real results (not just test sample results)
@mock.patch("datasources.bjs_incarceration.load_tables", side_effect=_get_test_table_files)
@mock.patch("ingestion.gcs_to_bq_util.add_df_to_bq", return_value=None)
def testWriteToBqNetworkCalls(
    mock_bq: mock.MagicMock,
    mock_zip: mock.MagicMock,
):
    datasource = BJSIncarcerationData()

    # required by bigQuery
    kwargs = {
        "filename": "test_file.csv",
        "metadata_table_id": "test_metadata",
        "table_name": "output_table",
    }

    datasource.write_to_bq("dataset", "gcs_bucket", **kwargs)

    assert mock_bq.call_count == 6
    assert mock_zip.call_count == 2

    (df_age_national, _, table_name_age_national) = mock_bq.call_args_list[0].args
    assert df_age_national.shape == (14, 12)
    assert table_name_age_national == "age_national_current"

    (df_race_national, _, table_name_race_national) = mock_bq.call_args_list[1].args
    # BJS drops the race_category_id column outside of the tested methods above,
    # so ensure that it's dropped before shipping to BQ
    assert (
        list(df_race_national.columns).sort()
        == [
            "prison_estimated_total",
            "state_name",
            "race_and_ethnicity",
            "prison_pct_share",
            "jail_estimated_total",
            "state_fips",
            "incarceration_population_estimated_total",
            "incarceration_population_pct",
            "prison_per_100k",
            "jail_per_100k",
            "jail_pct_share",
            "confined_children_estimated_total",
        ].sort()
    )
    assert table_name_race_national == "race_and_ethnicity_national_current"

    (df_sex_national, _, table_name_sex_national) = mock_bq.call_args_list[2].args
    assert df_sex_national.shape == (3, 12)
    assert table_name_sex_national == "sex_national_current"
