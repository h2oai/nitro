import { stylize as c } from './css'

it('should translate arbitrary values', () => {
  expect(c('w-[117px]')).toEqual('width:117px')
  // TODO
  // expect(c('grid-cols-[1fr_500px_2fr]')).toEqual('grid-template-columns:1fr 500px 2fr')
  // expect(c("bg-[#bada55]")).toEqual('--tw-bg-opacity:1;background-color:rgb(186 218 85 / var(--tw-bg-opacity)')
})

it('should translate color opacity', () => {
  expect(c('bg-indigo-500/75')).toEqual('--tw-bg-opacity:0.75;background-color:rgb(99 102 241 / var(--tw-bg-opacity))')
  expect(c('bg-black/75')).toEqual('--tw-bg-opacity:0.75;background-color:rgb(0 0 0 / var(--tw-bg-opacity))')
  expect(c('bg-white/75')).toEqual('--tw-bg-opacity:0.75;background-color:rgb(255 255 255 / var(--tw-bg-opacity))')
  expect(c('bg-accent-300/75')).toEqual('--tw-bg-opacity:0.75;background-color:rgb(var(--ui-accent-300) / var(--tw-bg-opacity))')
  // TODO
  // expect(c('grid-cols-[1fr_500px_2fr]')).toEqual('grid-template-columns:1fr 500px 2fr')
  // expect(c("bg-[#bada55]")).toEqual('--tw-bg-opacity:1;background-color:rgb(186 218 85 / var(--tw-bg-opacity)')
})

it('should translate stripes', () => {
  expect(c('bg-stripes-blue')).toEqual('background-color:rgb(96 165 250/.1);background-image:linear-gradient(135deg,rgb(59 130 246/.5) 10%,transparent 0,transparent 50%,rgb(59 130 246/.5) 0,rgb(59 130 246/.5) 60%,transparent 0,transparent);background-size:7.07px 7.07px')
  expect(c('bg-stripes-accent')).toEqual('background-color:rgb(var(--ui-accent-400)/.1);background-image:linear-gradient(135deg,rgb(var(--ui-accent-500)/.5) 10%,transparent 0,transparent 50%,rgb(var(--ui-accent-500)/.5) 0,rgb(var(--ui-accent-500)/.5) 60%,transparent 0,transparent);background-size:7.07px 7.07px')
})

it('should translate accent colors', () => {
  expect(c('bg-accent-300')).toEqual('--tw-bg-opacity:1;background-color:rgb(var(--ui-accent-300) / var(--tw-bg-opacity))')
})

it('should translate negative', () => {
  expect(c('-m-1')).toEqual('margin:-0.25rem')
  expect(c('-mx-1')).toEqual('margin-left:-0.25rem;margin-right:-0.25rem')
  expect(c('-my-1')).toEqual('margin-top:-0.25rem;margin-bottom:-0.25rem')
  expect(c('-mt-1')).toEqual('margin-top:-0.25rem')
  expect(c('-mr-1')).toEqual('margin-right:-0.25rem')
  expect(c('-mb-1')).toEqual('margin-bottom:-0.25rem')
  expect(c('-ml-1')).toEqual('margin-left:-0.25rem')
})