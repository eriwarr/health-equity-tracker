import type { Dataset } from './generateInsights'

const RATE_LIMIT_ENDPOINT = '/rate-limit-status'

export function extractMetadata(data: Dataset[]): {
  topic: string
  location: string
  demographic: string
} {
  const firstDataPoint = data[0] || {}

  const location = firstDataPoint.fips_name || 'United States'

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
    (k) => k !== 'fips_name' && k !== 'subgroup',
  )
  const firstMetricKey = dataKeys[0] || ''
  const topic = firstMetricKey
    .replace(
      /_pct_share|_population_pct|_per_100k|_rate|_estimated_total|_population/gi,
      '',
    )
    .replace(/_/g, ' ')
    .trim()

  return { topic, location, demographic }
}

export async function checkRateLimitStatus(): Promise<boolean> {
  const baseApiUrl = import.meta.env.VITE_BASE_API_URL
  const dataServerUrl = baseApiUrl
    ? `${baseApiUrl}${RATE_LIMIT_ENDPOINT}`
    : RATE_LIMIT_ENDPOINT
  try {
    const response = await fetch(dataServerUrl)

    if (!response.ok) {
      console.error('Failed to check rate limit status')
      return false
    }

    const data = await response.json()
    return data.rateLimitReached
  } catch (error) {
    console.error('Error checking rate limit status:', error)
    return false
  }
}
