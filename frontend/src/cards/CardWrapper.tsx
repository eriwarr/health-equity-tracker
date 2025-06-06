import { CircularProgress } from '@mui/material'
import type {
  MetricQuery,
  MetricQueryResponse,
} from '../data/query/MetricQuery'
import { WithMetadataAndMetrics } from '../data/react/WithLoadingOrErrorUI'
import type { MapOfDatasetMetadata } from '../data/utils/DatasetTypes'
import { SHOW_INSIGHT_GENERATION } from '../featureFlags'
import type { ScrollableHashId } from '../utils/hooks/useStepObserver'
import CardOptionsMenu from './ui/CardOptionsMenu'
import InsightDisplay from './ui/InsightDisplay'
import { Sources } from './ui/Sources'

function CardWrapper(props: {
  // prevent layout shift as component loads
  minHeight?: number
  downloadTitle: string
  infoPopover?: React.ReactNode
  hideFooter?: boolean
  hideNH?: boolean
  queries: MetricQuery[]
  loadGeographies?: boolean
  children: (
    queryResponses: MetricQueryResponse[],
    metadata: MapOfDatasetMetadata,
    geoData?: Record<string, any>,
    knownData?: Record<string, any>,
  ) => React.ReactNode
  isCensusNotAcs?: boolean
  scrollToHash: ScrollableHashId
  reportTitle: string
  expanded?: boolean
  isCompareCard?: boolean
  className?: string
  hasIntersectionalAllCompareBar?: boolean
  shareConfig?: any
  demographicType?: any
  metricIds?: any
}) {
  const loadingComponent = (
    <div
      className={`relative m-2 flex justify-center rounded bg-white p-3 shadow-raised ${props.className}`}
      style={{ minHeight: props.minHeight }}
      tabIndex={-1}
    >
      <CircularProgress aria-label='loading' />
    </div>
  )

  const shouldShowInsightDisplay = SHOW_INSIGHT_GENERATION && props.shareConfig

  return (
    <WithMetadataAndMetrics
      loadGeographies={props.loadGeographies}
      loadingComponent={loadingComponent}
      queries={props.queries ?? []}
    >
      {(metadata, queryResponses, geoData) => {
        return (
          <article
            className={`relative m-2 rounded-sm bg-white p-3 shadow-raised ${props.className}`}
          >
            {shouldShowInsightDisplay && (
              <InsightDisplay
                demographicType={props.demographicType}
                metricIds={props.metricIds}
                queryResponses={queryResponses}
                shareConfig={props.shareConfig}
              />
            )}
            <CardOptionsMenu
              reportTitle={props.reportTitle}
              scrollToHash={props.scrollToHash}
            />
            {props.children(queryResponses, metadata, geoData)}
            {!props.hideFooter && props.queries && (
              <Sources
                isCensusNotAcs={props.isCensusNotAcs}
                metadata={metadata}
                hideNH={props.hideNH}
                queryResponses={queryResponses}
                showDefinition={props.scrollToHash === 'rate-map'}
                isCompareCard={props.isCompareCard}
                hasIntersectionalAllCompareBar={
                  props.hasIntersectionalAllCompareBar
                }
              />
            )}
          </article>
        )
      }}
    </WithMetadataAndMetrics>
  )
}

export default CardWrapper
