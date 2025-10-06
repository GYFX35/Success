from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Listen for all console events and print them
    page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))

    # Verify agropastoral page
    print("--- Verifying agropastoral.html ---")
    page.goto("http://localhost:8080/agropastoral.html")
    agricultural_land_data_section = page.locator("#agricultural-land-data")
    expect(agricultural_land_data_section).to_contain_text("Brazil", timeout=10000)
    page.screenshot(path="/app/jules-scratch/verification/agropastoral.png")
    print("--- agropastoral.html OK ---")

    # Verify agroecology page
    print("--- Verifying agroecology.html ---")
    page.goto("http://localhost:8080/agroecology.html")
    agricultural_land_data_section_ecology = page.locator("#agricultural-land-data")
    expect(agricultural_land_data_section_ecology).to_contain_text("Brazil", timeout=10000)
    page.screenshot(path="/app/jules-scratch/verification/agroecology.png")
    print("--- agroecology.html OK ---")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)