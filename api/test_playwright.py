from playwright.sync_api import sync_playwright

print('Testing Playwright installation...')

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('https://www.baidu.com')
        title = page.title()
        print(f'Browser launched successfully! Page title: {title}')
        browser.close()
    print('Playwright test completed successfully!')
except Exception as e:
    print(f'Error: {e}')
    print('Playwright might not be installed properly.')
