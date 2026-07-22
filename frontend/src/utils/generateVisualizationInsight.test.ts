import type {
  DataTypeConfig,
  MetricConfig,
} from '../data/config/MetricConfigTypes'
import { MetricQueryResponse } from '../data/query/MetricQuery'
import type { HetRow } from '../data/utils/DatasetTypes'
import {
  buildInsightFocusSuffix,
  buildPrompt,
  formatDataRows,
  formatGeoComparisonRows,
  getInsightDataStatus,
  prepareInsightData,
} from './generateVisualizationInsight'

const DEMO = 'race_and_ethnicity'

const metricConfig = {
  metricId: 'rate',
  shortLabel: 'per 100k',
} as unknown as MetricConfig

const dataTypeConfig = {
  metrics: { per100k: metricConfig },
} as unknown as DataTypeConfig

describe('formatDataRows', () => {
  test('map rows are labeled with both place and demographic group, keeping "All"', () => {
    const rows: HetRow[] = [
      { fips_name: 'Gwinnett County', race_and_ethnicity: 'All', rate: 7.3 },
      {
        fips_name: 'Gwinnett County',
        race_and_ethnicity: 'Black (NH)',
        rate: 8.7,
      },
      {
        fips_name: 'Gwinnett County',
        race_and_ethnicity: 'White (NH)',
        rate: 6.6,
      },
    ]
    expect(formatDataRows(rows, 'rate-map', DEMO, metricConfig)).toEqual(
      '- Gwinnett County (All): 7.3 per 100k\n' +
        '- Gwinnett County (Black (NH)): 8.7 per 100k\n' +
        '- Gwinnett County (White (NH)): 6.6 per 100k',
    )
  })

  test('multi-region map labels each place with its demographic group', () => {
    const rows: HetRow[] = [
      { fips_name: 'Alabama', race_and_ethnicity: 'All', rate: 9 },
      { fips_name: 'Alaska', race_and_ethnicity: 'All', rate: 5 },
    ]
    expect(formatDataRows(rows, 'rate-map', DEMO, metricConfig)).toEqual(
      '- Alabama (All): 9 per 100k\n- Alaska (All): 5 per 100k',
    )
  })

  test('non-map charts label rows by demographic group alone', () => {
    const rows: HetRow[] = [
      { race_and_ethnicity: 'Black (NH)', rate: 9 },
      { race_and_ethnicity: 'White (NH)', rate: 13 },
    ]
    expect(formatDataRows(rows, 'data-table', DEMO, metricConfig)).toEqual(
      '- Black (NH): 9 per 100k\n- White (NH): 13 per 100k',
    )
  })

  test('time-series rows are filtered to the selected groups', () => {
    const rows: HetRow[] = [
      { race_and_ethnicity: 'Black (NH)', time_period: '2010', rate: 5 },
      { race_and_ethnicity: 'Black (NH)', time_period: '2020', rate: 8 },
      { race_and_ethnicity: 'White (NH)', time_period: '2010', rate: 3 },
      { race_and_ethnicity: 'White (NH)', time_period: '2020', rate: 4 },
    ]
    expect(
      formatDataRows(rows, 'rates-over-time', DEMO, metricConfig, [
        'Black (NH)',
      ]),
    ).toEqual(
      '- Black (NH) (2010): 5 per 100k\n- Black (NH) (2020): 8 per 100k',
    )
  })

  test('time-series with no selection includes every group', () => {
    const rows: HetRow[] = [
      { race_and_ethnicity: 'Black (NH)', time_period: '2010', rate: 5 },
      { race_and_ethnicity: 'White (NH)', time_period: '2010', rate: 3 },
    ]
    expect(formatDataRows(rows, 'rates-over-time', DEMO, metricConfig)).toEqual(
      '- Black (NH) (2010): 5 per 100k\n- White (NH) (2010): 3 per 100k',
    )
  })
})

describe('prepareInsightData', () => {
  test('a single-region map with only one labeled row yields one entry', () => {
    const response = new MetricQueryResponse([
      {
        fips_name: 'Bartow County',
        race_and_ethnicity: 'White (NH)',
        rate: 13,
      },
    ])
    const result = prepareInsightData('rate-map', dataTypeConfig, DEMO, [
      response,
    ])
    expect(result.entryCount).toBe(1)
    expect(result.dataSection).toEqual(
      '- Bartow County (White (NH)): 13 per 100k',
    )
  })

  test('a single-region map with several groups yields one entry per group', () => {
    const response = new MetricQueryResponse([
      { fips_name: 'Gwinnett County', race_and_ethnicity: 'All', rate: 7.3 },
      {
        fips_name: 'Gwinnett County',
        race_and_ethnicity: 'Black (NH)',
        rate: 8.7,
      },
      {
        fips_name: 'Gwinnett County',
        race_and_ethnicity: 'White (NH)',
        rate: 6.6,
      },
    ])
    const result = prepareInsightData('rate-map', dataTypeConfig, DEMO, [
      response,
    ])
    expect(result.entryCount).toBe(3)
  })

  test('time-series entry count respects the selected groups', () => {
    const response = new MetricQueryResponse([
      { race_and_ethnicity: 'Black (NH)', time_period: '2010', rate: 5 },
      { race_and_ethnicity: 'Black (NH)', time_period: '2020', rate: 8 },
      { race_and_ethnicity: 'White (NH)', time_period: '2010', rate: 3 },
      { race_and_ethnicity: 'White (NH)', time_period: '2020', rate: 4 },
    ])
    const result = prepareInsightData(
      'rates-over-time',
      dataTypeConfig,
      DEMO,
      [response],
      ['Black (NH)'],
    )
    // first + last year for the one selected group
    expect(result.entryCount).toBe(2)
  })
})

describe('getInsightDataStatus', () => {
  const oneRow = new MetricQueryResponse([
    { fips_name: 'Bartow County', race_and_ethnicity: 'All', rate: 13 },
  ])
  const twoRows = new MetricQueryResponse([
    { fips_name: 'Fulton County', race_and_ethnicity: 'All', rate: 9 },
    { fips_name: 'Bartow County', race_and_ethnicity: 'All', rate: 13 },
  ])
  const empty = new MetricQueryResponse([])

  test("'multi' when two or more values are present", () => {
    expect(
      getInsightDataStatus('rate-map', dataTypeConfig, DEMO, [twoRows]),
    ).toBe('multi')
  })

  test("'single-region' when a map has exactly one value", () => {
    expect(
      getInsightDataStatus('rate-map', dataTypeConfig, DEMO, [oneRow]),
    ).toBe('single-region')
  })

  test("a single value on a non-map chart is 'empty', not 'single-region'", () => {
    // The parent-geography fallback only makes sense for maps, so a lone
    // value elsewhere stays hidden.
    expect(
      getInsightDataStatus('data-table', dataTypeConfig, DEMO, [oneRow]),
    ).toBe('empty')
  })

  test("'empty' when there is no usable data", () => {
    expect(
      getInsightDataStatus('rate-map', dataTypeConfig, DEMO, [empty]),
    ).toBe('empty')
  })

  test("'empty' when there is no query response at all", () => {
    expect(
      getInsightDataStatus('rate-map', dataTypeConfig, DEMO, undefined),
    ).toBe('empty')
  })
})

describe('formatGeoComparisonRows', () => {
  test('formats reference rates as prompt bullet lines', () => {
    expect(
      formatGeoComparisonRows([
        { label: 'Georgia (All)', value: 9.4, shortLabel: 'per 100k' },
        { label: 'United States (All)', value: 7.8, shortLabel: 'per 100k' },
      ]),
    ).toBe('- Georgia (All): 9.4 per 100k\n- United States (All): 7.8 per 100k')
  })

  test('empty input yields an empty string', () => {
    expect(formatGeoComparisonRows([])).toBe('')
  })
})

describe('buildInsightFocusSuffix', () => {
  test('empty when no context is given', () => {
    expect(buildInsightFocusSuffix()).toBe('')
    expect(buildInsightFocusSuffix({})).toBe('')
  })

  test('ignores an activeDemographicGroup of "All"', () => {
    expect(buildInsightFocusSuffix({ activeDemographicGroup: 'All' })).toBe('')
  })

  test('includes a non-All highlighted map group', () => {
    expect(
      buildInsightFocusSuffix({ activeDemographicGroup: 'Black (NH)' }),
    ).toBe('Black (NH)')
  })

  test('sorts selectedGroups so legend order does not change the key', () => {
    expect(
      buildInsightFocusSuffix({ selectedGroups: ['White (NH)', 'Black (NH)'] }),
    ).toBe('Black (NH),White (NH)')
    expect(
      buildInsightFocusSuffix({ selectedGroups: ['Black (NH)', 'White (NH)'] }),
    ).toBe('Black (NH),White (NH)')
  })

  test('combines highlighted group and selected groups with a pipe', () => {
    expect(
      buildInsightFocusSuffix({
        activeDemographicGroup: 'Black (NH)',
        selectedGroups: ['White (NH)', 'Asian (NH)'],
      }),
    ).toBe('Black (NH)|Asian (NH),White (NH)')
  })

  test('empty selectedGroups array contributes nothing', () => {
    expect(buildInsightFocusSuffix({ selectedGroups: [] })).toBe('')
  })
})

describe('buildPrompt geo-context framing', () => {
  const args = [
    'rate-map',
    'Gun Deaths',
    'Bartow County, Georgia',
    'race and ethnicity',
    '- Bartow County (All): 13 per 100k\n- United States (All): 7.8 per 100k',
  ] as const

  test('names state and national only when both reference rates are present', () => {
    const prompt = buildPrompt(...args, undefined, 2)
    expect(prompt).toContain('its state and national averages')
    expect(prompt).toContain('against its state and the national average')
  })

  test('does not claim state and national when only one reference rate resolved', () => {
    const prompt = buildPrompt(...args, undefined, 1)
    expect(prompt).not.toContain('state and national')
    expect(prompt).not.toContain('the national average')
    expect(prompt).toContain('the reference average shown')
  })

  test('falls back to the standard disparity framing when no reference rates exist', () => {
    const prompt = buildPrompt(...args, undefined, 0)
    expect(prompt).not.toContain('reference average')
    expect(prompt).toContain('most important health equity disparity')
  })
})
