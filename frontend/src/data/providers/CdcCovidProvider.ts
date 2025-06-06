import { getDataManager } from '../../utils/globals'
import {
  AGE_ADJUST_COVID_DEATHS_US_SETTING,
  AGE_ADJUST_COVID_HOSP_US_SETTING,
} from '../../utils/internalRoutes'
import type { DataTypeId } from '../config/MetricConfigTypes'
import type { Breakdowns } from '../query/Breakdowns'
import {
  type MetricQuery,
  MetricQueryResponse,
  resolveDatasetId,
} from '../query/MetricQuery'
import { dropRecentPartialMonth } from '../utils/DatasetTimeUtils'
import { addAcsIdToConsumed, appendFipsIfNeeded } from '../utils/datasetutils'
import VariableProvider from './VariableProvider'

// when alternate data types are available, provide a link to the national level, by race report for that data type
export const dataTypeLinkMap: Partial<Record<DataTypeId, string>> = {
  covid_deaths: AGE_ADJUST_COVID_DEATHS_US_SETTING,
  covid_hospitalizations: AGE_ADJUST_COVID_HOSP_US_SETTING,
}
class CdcCovidProvider extends VariableProvider {
  constructor() {
    super(
      'cdc_covid_provider',
      [
        'covid_cases',
        'covid_deaths',
        'covid_hosp',
        'covid_cases_share',
        'covid_deaths_share',
        'covid_hosp_share',
        'covid_cases_share_of_known',
        'covid_deaths_share_of_known',
        'covid_hosp_share_of_known',
        'covid_deaths_per_100k',
        'covid_cases_per_100k',
        'covid_hosp_per_100k',
        'death_ratio_age_adjusted',
        'hosp_ratio_age_adjusted',
        'cases_ratio_age_adjusted',
        'covid_population_pct',
        'covid_cases_pct_relative_inequity',
        'covid_deaths_pct_relative_inequity',
        'covid_hosp_pct_relative_inequity',
      ], // TODO: remove unused items here; migrate to a COVID_METRICS or similar like other providers
    )
  }

  async getDataInternal(
    metricQuery: MetricQuery,
  ): Promise<MetricQueryResponse> {
    const { breakdowns, datasetId, isFallbackId } = resolveDatasetId(
      'cdc_restricted_data',
      '',
      metricQuery,
    )
    const { timeView } = metricQuery

    if (!datasetId) {
      return new MetricQueryResponse([], [])
    }

    const specificDatasetId = isFallbackId
      ? datasetId
      : appendFipsIfNeeded(datasetId, breakdowns)
    const covidDataset = await getDataManager().loadDataset(specificDatasetId)
    const consumedDatasetIds = [datasetId]
    let df = covidDataset.toDataFrame()

    df = this.filterByGeo(df, breakdowns)

    if (df.toArray().length === 0) {
      return new MetricQueryResponse([], consumedDatasetIds)
    }
    df = this.renameGeoColumns(df, breakdowns)

    if (timeView === 'historical') {
      df = dropRecentPartialMonth(df)
    }

    /* We use DECIA_2020 populations OR ACS on the backend; add the correct id so footer is correct */
    const isIslandArea = breakdowns.filterFips?.isIslandArea()

    // TODO: this should be a reusable function that can work for all Providers
    if (isIslandArea) {
      if (breakdowns.hasOnlyRace()) {
        if (breakdowns.geography === 'state') {
          consumedDatasetIds.push(
            'decia_2020_territory_population-race_and_ethnicity_state_current',
          )
        }
        if (breakdowns.geography === 'county') {
          consumedDatasetIds.push(
            'decia_2020_territory_population-race_and_ethnicity_county_current',
          )
        }
      }

      if (breakdowns.hasOnlySex()) {
        if (breakdowns.geography === 'state') {
          consumedDatasetIds.push(
            'decia_2020_territory_population-sex_state_current',
          )
        }
        if (breakdowns.geography === 'county') {
          consumedDatasetIds.push(
            'decia_2020_territory_population-sex_county_current',
          )
        }
      }

      if (breakdowns.hasOnlyAge()) {
        if (breakdowns.geography === 'state') {
          consumedDatasetIds.push(
            'decia_2020_territory_population-age_state_current',
          )
        }
        if (breakdowns.geography === 'county') {
          consumedDatasetIds.push(
            'decia_2020_territory_population-age_county_current',
          )
        }
      }
    } else {
      addAcsIdToConsumed(metricQuery, consumedDatasetIds)
    }

    if (isFallbackId) {
      df = this.castAllsAsRequestedDemographicBreakdown(df, breakdowns)
    } else {
      df = this.applyDemographicBreakdownFilters(df, breakdowns)
      df = this.removeUnrequestedColumns(df, metricQuery)
    }

    return new MetricQueryResponse(df.toArray(), consumedDatasetIds)
  }

  allowsBreakdowns(breakdowns: Breakdowns): boolean {
    return breakdowns.hasExactlyOneDemographic()
  }
}
export default CdcCovidProvider
