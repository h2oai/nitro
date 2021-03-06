from pathlib import Path
from playwright.sync_api import sync_playwright

url = 'http://localhost:5000'
output_dir = Path('docs') / 'assets' / 'screenshots'

output_dir.mkdir(exist_ok=True)

with sync_playwright() as p:
    print('Launching browser...')
    browser = p.chromium.launch()
    page = browser.new_page()

    print(f'Navigating to {url} ...')
    page.goto(url)

    link_prefix = '#!docs.help_'
    all_links = page.locator('a[href]').element_handles()
    all_hrefs = [link.get_attribute('href') for link in all_links]
    example_hrefs = [href for href in all_hrefs if href.startswith(link_prefix)]
    example_names = [href[len(link_prefix):] for href in example_hrefs]
    print(f'Collected {len(example_names)} examples.')

    for name, href in zip(example_names, example_hrefs):
        if name.endswith('_noop'):
            continue
        print(f'Capturing {name}...')
        page.locator(f'[href="{href}"]').click()
        page.wait_for_timeout(1000)
        page.locator('[data-name=output]').screenshot(path=str(output_dir / f'{name}.png'))
        page.locator('[data-name=contents]').click()
    browser.close()
    print('Done!')
