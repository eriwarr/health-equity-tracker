import PhoneIcon from '@mui/icons-material/Phone'
import type { DataTypeId } from '../../data/config/MetricConfigTypes'
import HetNotice from '../../styles/HetComponents/HetNotice'
import { urlMap } from '../../utils/externalUrls'

export const LIFELINE_IDS: DataTypeId[] = ['suicide', 'gun_violence_suicide']

export default function LifelineAlert() {
  return (
    <HetNotice
      className='mx-2 mt-4 mb-2 border border-secondary-main text-left text-small lg:mt-4 lg:mb-4 lg:ml-2'
      icon={<PhoneIcon color='primary' />}
      title='988 Suicide & Crisis Lifeline'
      kind='text-only'
    >
      <p>
        For 24/7, free and confidential support, prevention and crisis
        resources, and professional best practices, call{' '}
        <a href='tel:988'>9-8-8</a> or visit{' '}
        <a href={urlMap.lifeline}>988lifeline.org</a>. If you or a loved one is
        experiencing an emergency, call 911 or go to your nearest emergency
        room.
      </p>
    </HetNotice>
  )
}
