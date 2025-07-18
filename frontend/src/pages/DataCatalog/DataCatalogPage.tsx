import {
  type DataSourceId,
  dataSourceMetadataMap,
} from '../../data/config/MetadataMap'
import { WithMetadata } from '../../data/react/WithLoadingOrErrorUI'
import type { DataSourceMetadata } from '../../data/utils/DatasetTypes'
import HetCTASmall from '../../styles/HetComponents/HetCTASmall'
import HetTextArrowLink from '../../styles/HetComponents/HetTextArrowLink'
import {
  DATA_CATALOG_PAGE_LINK,
  EXPLORE_DATA_PAGE_LINK,
} from '../../utils/internalRoutes'
import { DATA_SOURCE_PRE_FILTERS, useSearchParams } from '../../utils/urlutils'
import DataSourceListing from './DataSourceListing'

// Map of filter id to list of datasets selected by that filter, or empty list
// for filters that don't have anything selected.
type Filters = Record<string, DataSourceId[]>

// The id of the filter by dataset name. This is the only one that supports
// pre-filtering from url params.
const NAME_FILTER_ID = 'name_filter'

/**
 * Returns the ids of the sources to display based on the provided filter. The
 * displayed sources are the intersection of each filter.
 */
function getFilteredSources(
  metadata: Record<DataSourceId, DataSourceMetadata>,
  activeFilter: Filters,
): DataSourceId[] {
  const filters = Object.values(activeFilter)
  const reducer = (
    intersection: DataSourceId[],
    nextFilter: DataSourceId[],
  ) => {
    if (nextFilter.length === 0) {
      return intersection
    }
    return intersection.filter((x) => nextFilter.includes(x))
  }
  const allIds = Object.keys(metadata) as DataSourceId[]
  return filters.reduce(reducer, allIds)
}

export default function DataCatalogPage() {
  const params = useSearchParams()
  const datasets = params[DATA_SOURCE_PRE_FILTERS]
    ? params[DATA_SOURCE_PRE_FILTERS].split(',')
    : []

  const activeFilter = {
    [NAME_FILTER_ID]: datasets as DataSourceId[],
  }

  return (
    <>
      <title>Data Downloads - Health Equity Tracker</title>
      <section
        id='main-content'
        className='mx-auto flex w-svw max-w-lgplus flex-col justify-center px-2 py-16 sm:px-16 md:px-24 lg:px-56'
      >
        <h1
          id='main'
          className='font-bold font-sans-title text-alt-green text-big-header leading-normal'
        >
          Data Downloads
        </h1>

        <p className='text-text'>
          Here you can access and download the data source files that are
          displayed in the charts on the Health Equity Tracker. Want to explore
          what each data set can show us about different health outcomes?
        </p>

        <HetCTASmall
          className='mx-auto w-fit font-extrabold'
          href={EXPLORE_DATA_PAGE_LINK}
        >
          Explore the data dashboard
        </HetCTASmall>
        <ul className='list-none pl-0'>
          <WithMetadata>
            {(datasetMetadata) => {
              const filteredDatasets = getFilteredSources(
                dataSourceMetadataMap,
                activeFilter,
              )
              // Check if more than the default filters are enabled to see if you're viewing
              // a subset of sources
              const viewingSubsetOfSources =
                Object.keys(activeFilter).length > 1 ||
                activeFilter[NAME_FILTER_ID].length > 0

              return (
                <>
                  {filteredDatasets.map((sourceId) => (
                    <li key={sourceId}>
                      <DataSourceListing
                        key={dataSourceMetadataMap[sourceId].id}
                        source_metadata={dataSourceMetadataMap[sourceId]}
                        dataset_metadata={datasetMetadata}
                      />
                    </li>
                  ))}
                  {viewingSubsetOfSources && (
                    <HetTextArrowLink
                      containerClassName='flex justify-center'
                      link={DATA_CATALOG_PAGE_LINK}
                      linkText={'View All Datasets'}
                    />
                  )}
                </>
              )
            }}
          </WithMetadata>
        </ul>
      </section>
    </>
  )
}
