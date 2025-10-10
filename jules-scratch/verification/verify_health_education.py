from playwright.sync_api import sync_playwright, expect
import os

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the new solutions page
        page.goto("http://localhost:8080/health_education.html")

        # Wait for the life expectancy chart and child mortality data to be visible
        expect(page.locator("#life-expectancy-chart-container canvas")).to_be_visible(timeout=30000)
        expect(page.locator("#child-mortality-chart-container pre")).to_be_visible(timeout=30000)

        # Take a screenshot
        screenshot_path = "jules-scratch/verification/health_education.png"
        page.screenshot(path=screenshot_path)

        browser.close()

        if os.path.exists(screenshot_path):
            print(f"Screenshot saved to {screenshot_path}")
        else:
            print("Screenshot not saved.")

if __name__ == "__main__":
    run_verification()