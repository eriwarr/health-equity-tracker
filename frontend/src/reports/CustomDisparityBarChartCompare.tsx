import type React from 'react'
import DisparityBarChartCard from '../cards/DisparityBarChartCard'
import { Fips } from '../data/utils/Fips'
import { METRIC_CONFIG, type DataTypeConfig } from '../data/config/MetricConfig'

const CustomDisparityBarChartCompare: React.FC = () => {
  const fipsFlorida = new Fips('12')
  const fipsCalifornia = new Fips('06')
  const dataTypeConfig: DataTypeConfig = METRIC_CONFIG['health_insurance'][0]

  return (
    <div style={{ display: 'flex', justifyContent: 'space-around' }}>
      <div style={{ flex: 1, margin: '0 10px' }}>
        <DisparityBarChartCard
          dataTypeConfig={dataTypeConfig}
          demographicType='sex'
          fips={fipsFlorida}
          reportTitle={`Uninsurance in Florida by Sex`}
        />
      </div>
      <div style={{ flex: 1, margin: '0 10px' }}>
        <DisparityBarChartCard
          dataTypeConfig={dataTypeConfig}
          demographicType='sex'
          fips={fipsCalifornia}
          reportTitle={`Uninsurance in FL & CA by Sex`}
        />
      </div>
    </div>
  )
}

export default CustomDisparityBarChartCompare