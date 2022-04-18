from pathlib import Path
from playwright.sync_api import sync_playwright

url = 'http://localhost:3000'
output_dir = Path('docs') / 'assets' / 'screenshots'

output_dir.mkdir(exist_ok=True)

with sync_playwright() as p:
    print('Launching browser...')
    browser = p.chromium.launch()
    page = browser.new_page()

    print(f'Navigating to {url} ...')
    page.goto(url)

    example_links = page.locator('[data-jump]').element_handles()
    example_names = [link.get_attribute('data-jump') for link in example_links]
    print(f'Collected {len(example_names)} examples.')

    for name in example_names:
        print(f'Capturing {name}...')
        page.locator(f'[data-jump={name}]').click()
        page.locator('[data-name=output]').screenshot(path=str(output_dir / f'{name}.png'))
        page.locator('[data-name=contents]').click()
    browser.close()
    print('Done!')
