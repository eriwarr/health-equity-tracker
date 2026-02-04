import type { MetricId } from '../data/config/MetricConfigTypes'
import { SHOW_INSIGHT_GENERATION } from '../featureFlags'
import type { ChartData } from '../reports/Report'
import {
  extractRelevantData,
  getHighestDisparity,
} from './generateInsightsUtils'

const API_ENDPOINT = '/fetch-ai-insight'
const ERROR_GENERATING_INSIGHT = 'Error generating insight'

export type Dataset = Record<string, any>

export interface Disparity {
  disparity: number
  location: string
  measure: string
  outcomeShare: number
  populationShare: number
  ratio: number
  subgroup: string
}

export interface ResultData {
  fips_name: string
  race_and_ethnicity?: string
  age?: string | number
  sex?: string
  [key: string]: any
}

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

    // Backend now returns Claude's response in the 'content' field
    if (!insight.content) {
      throw new Error('No content returned from AI service')
    }

    const content = insight.content.trim()

    return content
  } catch (error) {
    console.error('Error generating insight:', error)
    return ERROR_GENERATING_INSIGHT
  }
}

function generateInsightPrompt(disparities: Disparity): string {
  const { subgroup, location, measure, populationShare, outcomeShare, ratio } =
    disparities

  return `You are a public health data analyst. Analyze this health disparity data and provide a clear, accessible insight.

Data:
- Subgroup: ${subgroup}
- Location: ${location}
- Health Measure: ${measure}
- Population Share: ${populationShare}%
- Health Outcome Share: ${outcomeShare}%
- Disparity Ratio: ${ratio}:1

Please write a single, clear paragraph (2-3 sentences) that:
1. States the disparity using contrasting language (e.g., "but", "while", "however")
2. Makes the real-world impact clear
3. Uses plain language accessible to both practitioners and community members
4. Adapts the measure name to fit grammatically (e.g., "uninsured cases", "HIV deaths", "PrEP prescriptions")

Note: If the measure is PrEP, the population share represents PrEP-eligible population and the outcome is PrEP prescriptions.

Example format: "In ${location}, ${subgroup} individuals make up ${populationShare}% of the population but account for ${outcomeShare}% of ${measure}, making them ${ratio} times more likely to experience this health outcome."

Provide only the insight paragraph, no preamble or additional formatting.`
}

function mapRelevantData(
  dataArray: Dataset[],
  metricIds: MetricId[],
): ResultData[] {
  return dataArray.map((dataset) => extractRelevantData(dataset, metricIds))
}

export async function generateInsight(
  chartMetrics: ChartData,
): Promise<string> {
  if (!SHOW_INSIGHT_GENERATION) {
    return ''
  }

  try {
    const { knownData, metricIds } = chartMetrics
    const processedData = mapRelevantData(knownData, metricIds)
    const highestDisparity = getHighestDisparity(processedData)
    const insightPrompt = generateInsightPrompt(highestDisparity)
    return await fetchAIInsight(insightPrompt)
  } catch (error) {
    console.error(ERROR_GENERATING_INSIGHT, error)
    return ERROR_GENERATING_INSIGHT
  }
}
