import { CDC_CANCER_CATEGORY_DROPDOWNIDS } from '../../../data/config/MetricConfigCancer'
import StripedTable from '../methodologyComponents/StripedTable'
import { buildTopicsString } from './linkUtils'

export const cancerTopicString = buildTopicsString(
  CDC_CANCER_CATEGORY_DROPDOWNIDS,
)

const CancerLink = () => {
  return (
    <section id='cancer'>
      <title>Cancer - Health Equity Tracker</title>
      <article>
        <StripedTable
          id='categories-table'
          applyThickBorder={false}
          columns={[
            { header: 'Category', accessor: 'category' },
            { header: 'Topics', accessor: 'topic' },
          ]}
          rows={[
            {
              category: 'Cancer',
              topic: cancerTopicString,
            },
          ]}
        />
      </article>
    </section>
  )
}

export default CancerLink
