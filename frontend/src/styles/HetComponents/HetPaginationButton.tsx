import { ArrowBack, ArrowForward } from '@mui/icons-material'
import { Button } from '@mui/material'

type HetPaginationDirection = 'previous' | 'next'

interface HetPaginationButtonsProps {
  direction: HetPaginationDirection
  onClick: () => void
  children?: React.ReactNode | string
  disabled?: boolean
  className?: string
}

export default function HetPaginationButton({
  direction,
  onClick,
  children,
  disabled,
  className,
}: HetPaginationButtonsProps) {
  const isPrevious = direction === 'previous'

  return (
    <Button
      onClick={onClick}
      disabled={disabled}
      className={`my-2 flex h-24 max-h-32 min-h-24 flex-col justify-center rounded-3xl bg-methodology-green font-medium font-sans-title text-alt-black leading-some-more-space tracking-wide shadow-raised-tighter hover:shadow-raised sm:w-auto smplus:w-full md:w-80 lg:mb-0 ${className}`}
    >
      {/* ARROW AND DIRECTION WORD */}
      <span
        className={`mt-5 flex items-center self-stretch font-sans-text text-alt-black text-small leading-loose lg:leading-some-more-space ${
          isPrevious ? 'ml-5 justify-start' : 'mr-5 justify-end'
        }`}
      >
        {isPrevious ? (
          <span className='flex align-center'>
            <ArrowBack /> <span>Previous</span>
          </span>
        ) : (
          <span className='flex align-center'>
            <span>Up Next</span> <ArrowForward />
          </span>
        )}
      </span>
      {/* LABEL FOR LINKED PAGE */}
      <span className='mb-5 flex shrink-0 flex-col justify-center gap-2 self-stretch p-2 font-semibold text-text leading-normal'>
        <span
          className={
            isPrevious
              ? 'ml-5 items-start justify-start text-left'
              : 'mr-5 items-end justify-end text-right'
          }
          data-pagination-content='true'
        >
          {children}
        </span>
      </span>
    </Button>
  )
}
