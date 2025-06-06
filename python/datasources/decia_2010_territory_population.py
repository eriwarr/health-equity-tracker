import ingestion.standardized_columns as std_col
from datasources.data_source import DataSource
from ingestion import gcs_to_bq_util, constants
from ingestion.dataset_utils import generate_pct_share_col_without_unknowns
from ingestion.standardized_columns import Race

# The 2010 ACS datasets for the smaller territories need to be manually downloaded as zip files
# and particular values extracted from the html into json in the /data folder for processing

# https://www.census.gov/data/datasets/2010/dec/american-samoa.html RACE: /AS/AS8_0000001_040.html
# https://www.census.gov/data/datasets/2010/dec/guam.html RACE: /GU/GU8_0000001_040.html
# https://www.census.gov/data/datasets/2010/dec/virgin-islands.html RACE: VI/VI8_0000001_040.html
# https://www.census.gov/data/datasets/2010/dec/cnmi.html RACE: CNMI/MP8_0000001_040.html

source_data_files = [
    "decia_2010_territory_population-race_and_ethnicity_territory.json",
    "decia_2010_territory_population-sex_territory.json",
    "decia_2010_territory_population-age_territory.json",
]


def get_breakdown_col(df):
    if std_col.RACE_CATEGORY_ID_COL in df.columns:
        return std_col.RACE_CATEGORY_ID_COL
    elif std_col.SEX_COL in df.columns:
        return std_col.SEX_COL
    elif std_col.AGE_COL in df.columns:
        return std_col.AGE_COL


class Decia2010TerritoryPopulationData(DataSource):
    @staticmethod
    def get_id():
        return "DECIA_2010_POPULATION"

    @staticmethod
    def get_table_name():
        return "decia_2010_territory_population"

    def upload_to_gcs(self, _, **attrs):
        raise NotImplementedError("upload_to_gcs should not be called for Decia2010TerritoryPopulationData")

    def write_to_bq(self, dataset, gcs_bucket, **attrs):

        for f in source_data_files:
            df = gcs_to_bq_util.load_json_as_df_from_data_dir("decia_2010_territory_population", f, {"state_fips": str})

            total_val = Race.ALL.value if get_breakdown_col(df) == std_col.RACE_CATEGORY_ID_COL else std_col.ALL_VALUE

            df = generate_pct_share_col_without_unknowns(
                df, {std_col.POPULATION_COL: std_col.POPULATION_PCT_COL}, get_breakdown_col(df), total_val
            )

            if std_col.RACE_CATEGORY_ID_COL in df.columns:
                std_col.add_race_columns_from_category_id(df)

            # Clean up column names.
            self.clean_frame_column_names(df)

            demo_type = next((demo for demo in ["sex", "age", "race_and_ethnicity"] if demo in f), None)
            table_id = gcs_to_bq_util.make_bq_table_id(demo_type, constants.STATE_LEVEL, constants.CURRENT)

            column_types = gcs_to_bq_util.get_bq_column_types(
                df, float_cols=[std_col.POPULATION_COL, std_col.POPULATION_PCT_COL]
            )
            gcs_to_bq_util.add_df_to_bq(df, dataset, table_id, column_types=column_types)
