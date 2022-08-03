import { stylize as c } from './css'

it('should translate arbitrary values', () => {
  expect(c('w-[117px]')).toEqual('width:117px')
  // TODO
  // expect(c('grid-cols-[1fr_500px_2fr]')).toEqual('grid-template-columns:1fr 500px 2fr')
  // expect(c("bg-[#bada55]")).toEqual('--tw-bg-opacity:1;background-color:rgb(186 218 85 / var(--tw-bg-opacity)')
})

it('should translate stripes', () => {
  expect(c('bg-stripes-blue')).toEqual('background-color:rgb(96 165 250/.1);background-image:linear-gradient(135deg,rgb(59 130 246/.5) 10%,transparent 0,transparent 50%,rgb(59 130 246/.5) 0,rgb(59 130 246/.5) 60%,transparent 0,transparent);background-size:7.07px 7.07px')
})

it('should translate UI colors', () => {
  expect(c('bg-ui-foreground')).toEqual('background-color:var(--ui-foreground)')
  expect(c('bg-ui-background')).toEqual('background-color:var(--ui-background)')
  expect(c('bg-ui-accent')).toEqual('background-color:var(--ui-accent)')
  expect(c('bg-ui-accent-darker')).toEqual('background-color:var(--ui-accent-darker)')
  expect(c('bg-ui-accent-dark')).toEqual('background-color:var(--ui-accent-dark)')
  expect(c('bg-ui-accent-dark-alt')).toEqual('background-color:var(--ui-accent-dark-alt)')
  expect(c('bg-ui-accent-primary')).toEqual('background-color:var(--ui-accent-primary)')
  expect(c('bg-ui-accent-secondary')).toEqual('background-color:var(--ui-accent-secondary)')
  expect(c('bg-ui-accent-tertiary')).toEqual('background-color:var(--ui-accent-tertiary)')
  expect(c('bg-ui-accent-light')).toEqual('background-color:var(--ui-accent-light)')
  expect(c('bg-ui-accent-lighter')).toEqual('background-color:var(--ui-accent-lighter)')
  expect(c('bg-ui-accent-lighter-alt')).toEqual('background-color:var(--ui-accent-lighter-alt)')
  expect(c('bg-ui-neutral-dark')).toEqual('background-color:var(--ui-neutral-dark)')
  expect(c('bg-ui-neutral-primary')).toEqual('background-color:var(--ui-neutral-primary)')
  expect(c('bg-ui-neutral-primary-alt')).toEqual('background-color:var(--ui-neutral-primary-alt)')
  expect(c('bg-ui-neutral-secondary')).toEqual('background-color:var(--ui-neutral-secondary)')
  expect(c('bg-ui-neutral-secondary-alt')).toEqual('background-color:var(--ui-neutral-secondary-alt)')
  expect(c('bg-ui-neutral-tertiary')).toEqual('background-color:var(--ui-neutral-tertiary)')
  expect(c('bg-ui-neutral-tertiary-alt')).toEqual('background-color:var(--ui-neutral-tertiary-alt)')
  expect(c('bg-ui-neutral-quaternary')).toEqual('background-color:var(--ui-neutral-quaternary)')
  expect(c('bg-ui-neutral-quaternary-alt')).toEqual('background-color:var(--ui-neutral-quaternary-alt)')
  expect(c('bg-ui-neutral-light')).toEqual('background-color:var(--ui-neutral-light)')
  expect(c('bg-ui-neutral-lighter')).toEqual('background-color:var(--ui-neutral-lighter)')
  expect(c('bg-ui-neutral-lighter-alt')).toEqual('background-color:var(--ui-neutral-lighter-alt)')
})
