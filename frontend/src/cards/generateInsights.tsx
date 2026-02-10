// generateInsights.ts

import type { MetricId } from '../data/config/MetricConfigTypes'
import type { Fips } from '../data/utils/Fips'
import { SHOW_INSIGHT_GENERATION } from '../featureFlags'
import type { ChartData } from '../reports/Report'
import type { ScrollableHashId } from '../utils/hooks/useStepObserver'

const API_ENDPOINT = '/fetch-ai-insight'
const ERROR_GENERATING_INSIGHT = 'Error generating insight'

export type Dataset = Record<string, any>

async function fetchAIInsight(prompt: string): Promise<string> {
  const baseApiUrl = import.meta.env.VITE_BASE_API_URL
  const dataServerUrl = baseApiUrl
    ? `${baseApiUrl}${API_ENDPOINT}`
    : API_ENDPOINT

  if (!SHOW_INSIGHT_GENERATION) {
    return ''
  }

  try {
    const dataResponse = await fetch(dataServerUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt }),
    })

    if (!dataResponse.ok) {
      if (dataResponse.status === 429) {
        return 'AI insights temporarily unavailable due to rate limits. Please try again later.'
      }
      throw new Error(`Failed to fetch AI insight: ${dataResponse.statusText}`)
    }

    const insight = await dataResponse.json()

    if (!insight.content) {
      throw new Error('No content returned from AI service')
    }

    return insight.content.trim()
  } catch (error) {
    console.error('Error generating insight:', error)
    return ERROR_GENERATING_INSIGHT
  }
}

function extractMetadata(data: Dataset[]): {
  topic: string
  demographic: string
} {
  const firstDataPoint = data[0] || {}

  let demographic = 'overall population'
  if (firstDataPoint.subgroup) {
    const subgroup = firstDataPoint.subgroup
    if (subgroup.includes('(NH)') || subgroup.includes('Latino')) {
      demographic = 'race and ethnicity'
    } else if (!isNaN(Number(subgroup)) || subgroup.includes('-')) {
      demographic = 'age group'
    } else if (subgroup === 'Male' || subgroup === 'Female') {
      demographic = 'sex'
    }
  }

  // Extract topic from the data keys
  const dataKeys = Object.keys(firstDataPoint).filter(
    (k) => k !== 'fips_name' && k !== 'subgroup' && k !== 'time_period',
  )
  const firstMetricKey = dataKeys[0] || ''
  const topic = firstMetricKey
    .replace(
      /_pct_share|_population_pct|_per_100k|_rate|_estimated_total|_population/gi,
      '',
    )
    .replace(/_/g, ' ')
    .trim()

  return { topic, demographic }
}

function generateInsightPrompt(
  topic: string,
  location: string,
  demographic: string,
  formattedData: string,
  hashId: ScrollableHashId,
): string {
  return `Analyze health data about ${topic} in ${location} for ${demographic} with this data: ${formattedData}.

Write a single, clear paragraph (2-3 sentences) that identifies the most significant disparity or pattern and makes the real-world impact clear using plain language for our ${hashId} chart.`
}

function mapRelevantData(
  dataArray: Dataset[],
  metricIds: MetricId[],
): Dataset[] {
  return dataArray.map((dataset) => {
    const { fips_name, race_and_ethnicity, age, sex, time_period, ...rest } =
      dataset
    const result: Dataset = { fips_name }

    // Add demographic field
    const subgroup = race_and_ethnicity || age || sex
    if (subgroup) {
      result.subgroup = subgroup
    }

    // Preserve time_period if it exists
    if (time_period !== undefined) {
      result.time_period = time_period
    }

    // Add metric values
    metricIds.forEach((metricId) => {
      result[metricId] = rest[metricId]
    })

    return result
  })
}

export async function generateInsight(
  chartMetrics: ChartData,
  hashId: ScrollableHashId,
  fips?: Fips,
): Promise<string> {
  if (!SHOW_INSIGHT_GENERATION) {
    return ''
  }

  try {
    const { knownData, metricIds } = chartMetrics

    if (!knownData || knownData.length === 0) {
      return 'No data available to generate insights.'
    }

    const processedData = mapRelevantData(knownData, metricIds)
    const { topic, demographic } = extractMetadata(processedData)
    const location = fips?.getDisplayName() || ''
    const formattedData = JSON.stringify(processedData, null, 2)
    const prompt = generateInsightPrompt(
      topic,
      location,
      demographic,
      formattedData,
      hashId,
    )

    return await fetchAIInsight(prompt)
  } catch (error) {
    console.error(ERROR_GENERATING_INSIGHT, error)
    return ERROR_GENERATING_INSIGHT
  }
}
