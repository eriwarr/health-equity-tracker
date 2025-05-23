from enum import Enum, unique
from collections import namedtuple
import pandas as pd  # type: ignore
from typing import List
from ingestion.het_types import WISQARS_VAR_TYPE

# The name of the column for a unique string id for the race category. Should be
# semi-human readable. See Race enum below for values.
RACE_CATEGORY_ID_COL = "race_category_id"

# The name of the column that displays the fully-qualified race name, including
# whether Hispanic/Latino are included.
RACE_OR_HISPANIC_COL = "race_and_ethnicity"

# The name of the column for Whether a person is Hispanic/Latino or not.
HISPANIC_COL = "hispanic_or_latino"

# The name of the column that displays the basic race name, not specifying
# whether Hispanic/Latino people are included.
RACE_COL = "race"
ETH_COL = "ethnicity"
RACE_ETH_COL = "race_ethnicity_combined"
AGE_COL = "age"
SEX_COL = "sex"

# DEMOGRAPHICS FOR BRFSS
INCOME_COL = "income"
EDUCATION_COL = "education"
INSURANCE_COL = "insurance_status"

# DEMOGRAPHICS FOR PHRMA
LIS_COL = "lis"
ELIGIBILITY_COL = "eligibility"

# DEMOGRAPHICS FOR WISQARS
URBANICITY_COL = "urbanicity"


STATE_FIPS_COL = "state_fips"
STATE_NAME_COL = "state_name"
STATE_POSTAL_COL = "state_postal"  # State 2-letter postal abbreviation.
COUNTY_FIPS_COL = "county_fips"
COUNTY_NAME_COL = "county_name"
POPULATION_COL = "population"
INCOME_COL = "income"
POPULATION_PCT_COL = "population_pct"
SVI = "svi"

TIME_PERIOD_COL = "time_period"

ALL_VALUE = "All"

# Covid cases, hospitalizations, and deaths columns
COVID_CASES = "cases"
COVID_HOSP_Y = "hosp_y"
COVID_HOSP_N = "hosp_n"
COVID_HOSP_UNKNOWN = "hosp_unknown"
COVID_DEATH_Y = "death_y"
COVID_DEATH_N = "death_n"
COVID_DEATH_UNKNOWN = "death_unknown"
COVID_POPULATION_PCT = "covid_population_pct"

PER_100K_SUFFIX = "per_100k"
PCT_RATE_SUFFIX = "pct_rate"
PCT_SHARE_SUFFIX = "pct_share"
SHARE_SUFFIX = "share"
SHARE_OF_KNOWN_SUFFIX = "share_of_known"
PCT_REL_INEQUITY_SUFFIX = "pct_relative_inequity"
RAW_SUFFIX = "estimated_total"
RAW_POP_SUFFIX = "population_estimated_total"
POP_PCT_SUFFIX = "population_pct"
RATIO_AGE_ADJUSTED_SUFFIX = "ratio_age_adjusted"
INDEX_SUFFIX = "index"

SUFFIXES_ALL_TIME_VIEWS = [
    PER_100K_SUFFIX,
    PCT_RATE_SUFFIX,
    INDEX_SUFFIX,
]
SUFFIXES_CURRENT_TIME_VIEWS = [
    PCT_SHARE_SUFFIX,
    RAW_SUFFIX,
    POP_PCT_SUFFIX,
    SHARE_OF_KNOWN_SUFFIX,
    RATIO_AGE_ADJUSTED_SUFFIX,
    POPULATION_COL,  # TODO: ideally we should refactor so all population count cols end with estimate_total
]

SUFFIXES_HISTORICAL_TIME_VIEWS = [
    PCT_REL_INEQUITY_SUFFIX,
]

SUFFIXES = SUFFIXES_ALL_TIME_VIEWS + SUFFIXES_CURRENT_TIME_VIEWS + SUFFIXES_HISTORICAL_TIME_VIEWS

COVID_CASES_PREFIX = "covid_cases"
COVID_HOSP_PREFIX = "covid_hosp"
COVID_DEATH_PREFIX = "covid_deaths"

COVID_DEATH_RATIO_AGE_ADJUSTED = "death_ratio_age_adjusted"
COVID_HOSP_RATIO_AGE_ADJUSTED = "hosp_ratio_age_adjusted"

UNINSURED_PER_100K_COL = "uninsured_per_100k"
UNINSURED_PCT_SHARE_COL = "uninsured_pct_share"
UNINSURED_POPULATION_PCT = "uninsured_population_pct"

UNINSURED_PREFIX = "uninsured"
POVERTY_PREFIX = "poverty"

ABOVE_POVERTY_COL = "above_poverty_line"
BELOW_POVERTY_COL = "below_poverty_line"


# prefixes for AHR columns
DEPRESSION_PREFIX = "depression"
ILLICIT_OPIOID_USE_PREFIX = "illicit_opioid_use"
NON_MEDICAL_RX_OPIOID_USE_PREFIX = "non_medical_rx_opioid_use"
NON_MEDICAL_DRUG_USE_PREFIX = "non_medical_drug_use"
EXCESSIVE_DRINKING_PREFIX = "excessive_drinking"
COPD_PREFIX = "copd"
DIABETES_PREFIX = "diabetes"
ANXIETY_PREFIX = "anxiety"
FREQUENT_MENTAL_DISTRESS_PREFIX = "frequent_mental_distress"
SUICIDE_PREFIX = "suicide"
PREVENTABLE_HOSP_PREFIX = "preventable_hospitalizations"
AVOIDED_CARE_PREFIX = "avoided_care"
CHRONIC_KIDNEY_PREFIX = "chronic_kidney_disease"
CARDIOVASCULAR_PREFIX = "cardiovascular_diseases"
ASTHMA_PREFIX = "asthma"
VOTER_PARTICIPATION_PREFIX = "voter_participation"

AHR_POPULATION_RAW = "ahr_population_estimated_total"
AHR_POPULATION_PCT = "ahr_population_pct"
CHR_POPULATION_RAW = "chr_population_estimated_total"
CHR_POPULATION_PCT = "chr_population_pct"

# Vaccination columns
VACCINATED_RAW = "vaccinated_estimated_total"
VACCINATED_PCT_RATE = "vaccinated_pct_rate"
VACCINATED_PCT_SHARE = "vaccinated_pct_share"
VACCINATED_POP_PCT = "vaccinated_pop_pct"
ACS_VACCINATED_POP_PCT = "acs_vaccinated_pop_pct"

# CAWP

# State Legislatures
PCT_OF_W_STLEG = "pct_share_of_women_state_leg"
PCT_OF_STLEG = "pct_share_of_state_leg"
W_STLEG_PCT_INEQUITY = "women_state_leg_pct_relative_inequity"
W_THIS_RACE_STLEG_COUNT = "women_this_race_state_leg_count"
W_THIS_RACE_STLEG_NAMES = "women_this_race_state_leg_names"
W_ALL_RACES_STLEG_COUNT = "women_all_races_state_leg_count"
W_ALL_RACES_STLEG_NAMES = "women_all_races_state_leg_names"
STLEG_COUNT = "total_state_leg_count"

# Congress
PCT_OF_W_CONGRESS = "pct_share_of_women_us_congress"
PCT_OF_CONGRESS = "pct_share_of_us_congress"
W_CONGRESS_PCT_INEQUITY = "women_us_congress_pct_relative_inequity"
W_THIS_RACE_CONGRESS_COUNT = "women_this_race_us_congress_count"
W_THIS_RACE_CONGRESS_NAMES = "women_this_race_us_congress_names"
W_ALL_RACES_CONGRESS_COUNT = "women_all_races_us_congress_count"
W_ALL_RACES_CONGRESS_NAMES = "women_all_races_us_congress_names"
CONGRESS_COUNT = "total_us_congress_count"
CONGRESS_NAMES = "total_us_congress_names"

# Incarceration columns
PRISON_PREFIX = "prison"
JAIL_PREFIX = "jail"
CHILDREN_PREFIX = "confined_children"
INCARCERATION_PREFIX = "incarceration"
CHILDREN_RAW = "confined_children_estimated_total"
JAIL_RAW = "jail_estimated_total"
PRISON_RAW = "prison_estimated_total"
JAIL_RATE = "jail_per_100k"
PRISON_RATE = "prison_per_100k"
JAIL_PCT_SHARE = "jail_pct_share"
PRISON_PCT_SHARE = "prison_pct_share"
INCARCERATION_POP_PCT_SHARE = "incarceration_population_pct"
INCARCERATION_POP_RAW = "incarceration_population_estimated_total"
JAIL_PCT_INEQUITY = "jail_pct_relative_inequity"
PRISON_PCT_INEQUITY = "prison_pct_relative_inequity"

# HIV
BLACK_WOMEN = "black_women"
HIV_BW_POPULATION_PCT = "black_women_population_pct"

HIV_POPULATION = "hiv_population"
HIV_POPULATION_PCT = "hiv_population_pct"


HIV_CARE_LINKAGE = "hiv_care_linkage"
HIV_CARE_POPULATION = "hiv_care_population"
HIV_CARE_POPULATION_PCT = "hiv_care_population_pct"
HIV_CARE_PREFIX = "hiv_care"
HIV_DEATHS_PREFIX = "hiv_deaths"
HIV_DIAGNOSES_PREFIX = "hiv_diagnoses"
HIV_PREP_COVERAGE = "hiv_prep_coverage"
# population of individuals with PrEP indicators
HIV_PREP_POPULATION = "hiv_prep_population"
HIV_PREP_POPULATION_PCT = "hiv_prep_population_pct"
HIV_PREP_PREFIX = "hiv_prep"
HIV_PREVALENCE_PREFIX = "hiv_prevalence"
HIV_STIGMA_INDEX = "hiv_stigma_index"
TOTAL_TRANS_MEN = "total_trans_men"
TOTAL_TRANS_WOMEN = "total_trans_women"
TOTAL_ADDITIONAL_GENDER = "total_additional_gender"
HIV_DEATH_RATIO_AGE_ADJUSTED = "hiv_deaths_ratio_age_adjusted"


# PHRMA
MEDICARE_PREFIX = "medicare"

# 100k
AMI_PREFIX = "medicare_ami"
PHRMA_HIV_PREFIX = "medicare_hiv"
SCHIZOPHRENIA_PREFIX = "medicare_schizophrenia"

# medication adherence
ANTI_PSYCHOTICS_PREFIX = "anti_psychotics"
ARV_PREFIX = "arv"
BETA_BLOCKERS_PREFIX = "beta_blockers"
CCB_PREFIX = "ccb"
DOAC_PREFIX = "doac"
BB_AMI_PREFIX = "bb_ami"
RASA_PREFIX = "ras_antagonists"
STATINS_PREFIX = "statins"

# Gun violence
FATAL_POPULATION = "fatal_population"
FATAL_POPULATION_PCT = "fatal_population_pct"
FATAL_PREFIX: WISQARS_VAR_TYPE = "fatal"

GUN_VIOLENCE_HOMICIDE_PREFIX: WISQARS_VAR_TYPE = "gun_violence_homicide"
GUN_VIOLENCE_HOMICIDE_RAW = "gun_violence_homicide_estimated_total"
GUN_VIOLENCE_HOMICIDE_PER_100K = "gun_violence_homicide_per_100k"
GUN_VIOLENCE_SUICIDE_PREFIX: WISQARS_VAR_TYPE = "gun_violence_suicide"
GUN_VIOLENCE_SUICIDE_RAW = "gun_violence_suicide_estimated_total"
GUN_VIOLENCE_SUICIDE_PER_100K = "gun_violence_suicide_per_100k"

# YOUNG ADULTS AND YOUTH
GUN_DEATHS_YOUNG_ADULTS_POP_PCT = "gun_deaths_young_adults_population_pct"
GUN_DEATHS_YOUNG_ADULTS_POPULATION = "gun_deaths_young_adults_population"
GUN_DEATHS_YOUNG_ADULTS_PREFIX: WISQARS_VAR_TYPE = "gun_deaths_young_adults"
GUN_DEATHS_YOUTH_POP_PCT = "gun_deaths_youth_population_pct"
GUN_DEATHS_YOUTH_POPULATION = "gun_deaths_youth_population"
GUN_DEATHS_YOUTH_PREFIX: WISQARS_VAR_TYPE = "gun_deaths_youth"

# BLACK MEN - HOMICIDES AND LAW ENFORCEMENT DEATHS
GUN_HOMICIDES_BM_RAW = "gun_homicides_black_men_estimated_total"
GUN_HOMICIDES_BM_POP_PCT = "gun_homicides_black_men_population_pct"
GUN_HOMICIDES_BM_POP_RAW = "gun_homicides_black_men_population_estimated_total"
GUN_HOMICIDES_BM_PER_100K = "gun_homicides_black_men_per_100k"
GUN_HOMICIDES_BM_PCT_SHARE = "gun_homicides_black_men_percent_share"
GUN_HOMICIDES_BM_PCT_REL_INEQUITY = "gun_homicides_black_men_pct_relative_inequity"


# MATERNAL MORTALITY
MM_PER_100K = "maternal_mortality_per_100k"
MATERNAL_DEATHS_RAW = "maternal_deaths_estimated_total"
LIVE_BIRTHS_RAW = "live_births_estimated_total"
MM_PCT_SHARE = "maternal_mortality_pct_share"
MM_PCT_REL_INEQUITY = "maternal_mortality_pct_relative_inequity"
MM_POP_PCT = "maternal_mortality_population_pct"


RaceTuple = namedtuple("RaceTuple", ["race_category_id", "race_and_ethnicity"])

RACE_COLUMNS = RaceTuple._fields


@unique
class Race(Enum):
    # These categories are one format of standard categories used in ACS data,
    # where categories are mutually exclusive but each one includes
    # Hispanic/Latino. The sum of these values is equal to the total population.
    # OTHER_STANDARD is defined as anyone who does not fall into one of the
    # other categories in this format.
    AIAN = ("AIAN", "Indigenous", True)
    ASIAN = ("ASIAN", "Asian", True)
    BLACK = ("BLACK", "Black or African American", True)
    NHPI = ("NHPI", "Native Hawaiian and Pacific Islander", True)
    MULTI = ("MULTI", "Two or more races", True)
    WHITE = ("WHITE", "White", True)
    OTHER_STANDARD = ("OTHER_STANDARD", "Unrepresented race", True)

    # These categories are another format of standard categories used in ACS
    # data, where categories are mutually exclusive and exclude Hispanic/Latino.
    # Hispanic/Latino is its own category. Each one of these is a strict subset
    # of its counterpart in the above format. OTHER_STANDARD_NH is defined as
    # anyone who does not fall into one of the other categories in this format.
    # Where possible, this format is preferred.
    AIAN_NH = ("AIAN_NH", "Indigenous", False)
    ASIAN_NH = ("ASIAN_NH", "Asian", False)
    BLACK_NH = ("BLACK_NH", "Black or African American", False)
    NHPI_NH = ("NHPI_NH", "Native Hawaiian and Pacific Islander", False)
    MULTI_NH = ("MULTI_NH", "Two or more races", False)
    WHITE_NH = ("WHITE_NH", "White", False)
    HISP = ("HISP", "Hispanic or Latino", True)
    OTHER_STANDARD_NH = ("OTHER_STANDARD_NH", "Unrepresented race", False)

    # Below are special values that have slightly different characteristics.

    # Hispanic vs Non-Hispanic can be defined differently across datasets.
    # Sometimes Hispanic/Latino is treated as mutually exclusive with other
    # racial categories, so when a person is categorized as Hispanic or Latino
    # they are excluded from the data for any other racial category they belong
    # to. Other times, a person may be reported as both Hispanic/Latino and as
    # another race. In some datasets, these are reported entirely independently
    # so we do not know the relationship between Hispanic/Latino and race.
    # ETHNICITY_UNKNOWN refers to data that does not know whether the person is
    # Hispanic or Latino. (Some datasets use "ethnicity" to refer to whether
    # someone is Hispanic or Latino).
    # PrEP data only collects data for the following race groups: Black, White,
    # Hispanic, and Other. The dataset does not distinguish what constitutes as other,
    # the other demographic does not include individuals who are hispanic.
    NH = ("NH", "Not Hispanic or Latino", False)
    ETHNICITY_UNKNOWN = ("ETHNICITY_UNKNOWN", "Unknown ethnicity", None)

    # OTHER_STANDARD and OTHER_STANDARD_NH define "other" in a specific way (see
    # above). Some datasets may group additional races into "other"
    # when reporting (for example "other" may sometimes include AIAN or NHPI).
    # These datasets should use OTHER_NONSTANDARD/OTHER_NONSTANDARD_NH to
    # prevent joining with the incorrect population data.
    # TODO: The frontend uses the race_and_ethnicity column as a unique
    # identifier in some places. Until we migrate to using race_category_id,
    # we add a * for the non-standard other so it doesn't accidentally get
    # joined with the standard other on the frontend.
    OTHER_NONSTANDARD = ("OTHER_NONSTANDARD", "Unrepresented race", True)
    OTHER_NONSTANDARD_NH = ("OTHER_NONSTANDARD_NH", "Unrepresented race", False)

    # CAWP Non-standard, non-exclusive Race/Eth Categories
    ASIAN_PAC = ("ASIAN_PAC", "Asian American & Pacific Islander", True)
    AIANNH = ("AIANNH", "Native American, Alaska Native, & Native Hawaiian", True)
    # Composite group needed for CAWP pct_relative_inequity calculations
    # which is equiv to the combo ACS categories AIAN + ASIAN + NHPI
    AIAN_API = (
        "AIAN_API",
        "American Indian, Alaska Native, Asian & Pacific Islander",
        True,
    )

    HISP_F = ("HISP_F", "Latina", True)
    MENA = ("MENA", "Middle Eastern & North African", True)

    # Categories that are combinations of other categories

    # Combines AIAN and NHPI
    API = ("API", "Asian, Native Hawaiian, and Pacific Islander", True)
    # Combines AIAN_NH and NHPI_NH
    API_NH = ("API_NH", "Asian, Native Hawaiian, and Pacific Islander", False)

    MULTI_OR_OTHER_STANDARD = (
        "MULTI_OR_OTHER_STANDARD",
        "Two or more races & Unrepresented race",
        True,
    )
    MULTI_OR_OTHER_STANDARD_NH = (
        "MULTI_OR_OTHER_STANDARD_NH",
        "Two or more races & Unrepresented race",
        False,
    )

    # When the race is unknown. Different from ETHNICITY_UNKNOWN, which
    # specifically refers to whether Hispanic/Latino is unknown.
    UNKNOWN = ("UNKNOWN", "Unknown race", True)
    UNKNOWN_NH = ("UNKNOWN_NH", "Unknown race", False)

    # The total across races. This must always be included when the other race
    # values do not sum to 100%
    ALL = ("ALL", ALL_VALUE, None)

    # We set the enum value to the first arg, which is the race category id, or
    # a unique code that can be used to reference that race. Race category ids
    # should be set to the same value as the enum name.
    # Arguments are set as optional to accommodate a mypy bug with enums:
    # https://github.com/python/mypy/issues/1021.
    def __new__(cls, value, race=None, includes_hispanic=None):
        obj = object.__new__(cls)
        obj._value_ = value
        obj._race = race
        obj._includes_hispanic = includes_hispanic
        return obj

    @property
    def race_category_id(self) -> str:
        """The race category id; uniquely identifies this enum member."""
        return self.value

    @property
    def race(self):
        """The basic display name for this race."""
        return self._race

    @property
    def includes_hispanic(self):
        """Whether this race includes Hispanic or Latino."""
        return self._includes_hispanic

    @property
    def race_and_ethnicity(self) -> str:
        """The fully-qualified display name that specifies both race and whether
        the category includes Hispanic or Latino."""
        if (
            self.includes_hispanic is True
            or self.includes_hispanic is None
            or self.race in ["Hispanic or Latino", "Not Hispanic or Latino"]
        ):
            return self.race
        else:
            return self.race + " (NH)"

    @staticmethod
    def get_col_names() -> list:
        """The list of column names for putting the race attributes into a
        table. Columns are returned in the same order as `as_tuple()`."""
        return list(RaceTuple._fields)

    @staticmethod
    def from_category_id(category_id: str):
        """Gets an instance of this Enum from the provided race category id."""
        # Instances of an enum can be constructed from their value, and since we
        # set the enum value to the category id, we can construct an instance
        # without providing other params.
        # pylint: disable=no-value-for-parameter
        return Race(category_id)

    def as_tuple(self) -> RaceTuple:
        """The race attributes, in the same order as `get_col_names()`."""
        return RaceTuple(self.race_category_id, self.race_and_ethnicity)


# TODO: Remove this function in favor of swap_race_id_col_for_names_col if possible
def add_race_columns_from_category_id(df):
    """Adds all race-related columns to the dataframe using the race category id
    to determine these values."""
    df["race_tuple"] = df.apply(lambda r: Race.from_category_id(r[RACE_CATEGORY_ID_COL]).as_tuple(), axis=1)
    df[Race.get_col_names()] = pd.DataFrame(df["race_tuple"].tolist(), index=df.index)
    df.drop("race_tuple", axis=1, inplace=True)


def swap_race_id_col_for_names_col(df):
    """Swaps the race category id column for the race_and_ethnicity col."""
    df["race_tuple"] = df.apply(lambda r: Race.from_category_id(r[RACE_CATEGORY_ID_COL]).as_tuple(), axis=1)
    df[Race.get_col_names()] = pd.DataFrame(df["race_tuple"].tolist(), index=df.index)
    df.drop("race_tuple", axis=1, inplace=True)
    df.drop(RACE_CATEGORY_ID_COL, axis=1, inplace=True)


def generate_column_name(prefix, suffix):
    """Generates a standard column name.

    prefix: A condition name
    suffix: a type of measurement (pct_share, per_100k)"""

    return f"{prefix}_{suffix}"


def extract_prefix(col_name: str) -> str:
    """Extracts the prefix from a column name that contains one of out standard HET suffixes."""

    for suffix in SUFFIXES:
        underscore_suffix = f"_{suffix}"
        if col_name.endswith(underscore_suffix):
            prefix = col_name[: -len(underscore_suffix)]
            return prefix

    raise ValueError(f"Column {col_name} does not contain a standard suffix from {SUFFIXES}")


def ends_with_suffix_from_list(col: str, suffixes: List[str]) -> bool:
    """Detects whether the given col name ends with ANY of the provided metric col suffixes"""
    return any(col.endswith(suffix) for suffix in suffixes)
