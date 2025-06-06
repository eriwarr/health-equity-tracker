import type { DemographicType } from '../query/Breakdowns'
import { AgeSorterStrategy } from './AgeSorterStrategy'
import { IncomeSorterStrategy } from './IncomeSorterStrategy'

type OptionalSortArgs = [
  compareFn?: ((a: string, b: string) => number) | undefined,
]

export function getSortArgs(
  demographicType: DemographicType,
): OptionalSortArgs {
  switch (demographicType) {
    case 'age':
      return [new AgeSorterStrategy(['All']).compareFn]
    case 'income':
      return [new IncomeSorterStrategy(['All', 'Under $15k']).compareFn]
    default:
      return []
  }
}
