#
# This script collects class names from tailwindcss.com and writes them to a html file.
#

htmlFile = 'tailwind.html'

fs = require 'fs'
{ webkit } = require 'playwright'

sleep = (ms) -> new Promise (r) -> setTimeout r, ms

collectSlugs = () ->
  await page.goto "https://tailwindcss.com/docs/installation"
  sublinks = await page.locator('nav ul ul a')
  n = await sublinks.count()
  slugs = []
  for i in [0 ... n]
    a = await sublinks.nth i
    slugs.push await a.getAttribute 'href'
  start = slugs.indexOf '/docs/aspect-ratio'
  end = slugs.indexOf '/docs/will-change'
  slugs.slice start, end + 1

collectNames = (names, slug) ->
  await sleep 750 * (1 + Math.random())
  console.log "Reading #{slug}..."
  await page.goto "https://tailwindcss.com#{slug}"
  cells = await page.locator('table').first().locator('td:first-child')
  names.push (await cells.allTextContents())...

collect = (slugs) ->
  names = []
  for slug in slugs
    await collectNames names, slug
  names

browser = await webkit.launch()
page = await browser.newPage()

console.log 'Collecting slugs...'
slugs = await collectSlugs()
console.log "Collected #{slugs.length} slugs"

names = await collect slugs

await browser.close()

html = names
  .map (name) -> "<div class='#{name}'/>"
  .join '\n'

fs.writeFileSync htmlFile, html, 'utf8'
console.log "Wrote  #{names.length} names to #{htmlFile}"
