
# Assignment 3 - Software Testing
# Tester: Niramon Kitrattanasak
# Test Case ID: T009
# Function: F9 - Product Comparison
# Scenario 2 (TC03-S2): Remove One Product from Comparison
# Tool: Python + Selenium WebDriver

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Products used for testing.
product_names = ["MacBook", "MacBook Air"]

# Screenshot evidence for this scenario.
screenshot_file = "F9_TC03_S2_Remove_One_Product.png"


# Step 1: Open Google Chrome using Selenium WebDriver.
driver = webdriver.Chrome()
driver.maximize_window()
driver.set_page_load_timeout(45)

try:
    # Open the MacBook search results.
    driver.get(
        "https://opencart.abstracta.us/"
        "index.php?route=product/search&search=MacBook"
    )

    # Wait for the product results.
    wait = WebDriverWait(driver, 30)

    wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "#content .product-layout")
        )
    )

    # Function to add a selected product to comparison.
    def add_to_comparison(product_name, expected_count):

        cards = driver.find_elements(
            By.CSS_SELECTOR,
            "#content .product-layout"
        )

        for card in cards:
            titles = card.find_elements(
                By.CSS_SELECTOR, "h4 a"
            )

            if not titles:
                continue

            if titles[0].text.strip() != product_name:
                continue

            # Find the Compare button.
            buttons = card.find_elements(
                By.CSS_SELECTOR,
                'button[onclick*="compare.add"]'
            )

            assert buttons, (
                f"Compare button not found for {product_name}"
            )

            compare_button = buttons[0]

            # Scroll to and click the Compare button.
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                compare_button
            )

            ActionChains(driver).move_to_element(
                compare_button
            ).perform()

            compare_button.click()

            # Wait for the comparison count to update.
            wait.until(
                lambda d: (
                    f"({expected_count})"
                    in d.find_element(
                        By.ID, "compare-total"
                    ).text
                )
            )

            print("Added to comparison:", product_name)
            return

        raise AssertionError(
            f"Product not found: {product_name}"
        )

    # Step 2: Add both products to the comparison list.
    add_to_comparison("MacBook", 1)
    add_to_comparison("MacBook Air", 2)

    # Step 3: Open the Product Comparison page.
    driver.get(
        "https://opencart.abstracta.us/"
        "index.php?route=product/compare"
    )

    wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "#content table")
        )
    )

    # Function to read the compared product names.
    def compared_products(browser):

        rows = browser.find_elements(
            By.XPATH,
            "//div[@id='content']//table//tr"
            "[td[1][normalize-space()='Product']]"
        )

        if not rows:
            return []

        cells = rows[0].find_elements(
            By.XPATH, "./td"
        )

        return [
            cell.text.strip()
            for cell in cells[1:]
        ]

    # Verify both products are present before removal.
    products_before = compared_products(driver)

    assert products_before == product_names, (
        f"Unexpected products before removal: {products_before}"
    )

    # Step 4: Find the Remove button for MacBook Air.
    remove_buttons = driver.find_elements(
        By.XPATH,
        "//div[@id='content']//table//a"
        "[contains(@href, 'remove=') "
        "and normalize-space()='Remove']"
    )

    assert len(remove_buttons) == 2, (
        f"Expected 2 Remove buttons, found {len(remove_buttons)}"
    )

    # Identify MacBook Air's column.
    product_index = products_before.index("MacBook Air")

    remove_button = remove_buttons[product_index]

    # Scroll to the correct Remove button.
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        remove_button
    )

    # Step 5: Remove MacBook Air.
    remove_button.click()

    # Step 6: Verify only MacBook remains.
    wait.until(
        lambda d: compared_products(d) == ["MacBook"]
    )

    products_after = compared_products(driver)

    assert products_after == ["MacBook"], (
        f"Unexpected products after removal: {products_after}"
    )

    # Step 7: Save screenshot evidence.
    driver.execute_script("window.scrollTo(0, 0);")
    driver.save_screenshot(screenshot_file)

    # Display test results in the terminal.
    print("\n========================================")
    print("Tester: Niramon Kitrattanasak")
    print("Test Case: T009")
    print("Function: F9 - Product Comparison")
    print("Scenario: TC03-S2 - Remove One Product")
    print("----------------------------------------")
    print("Expected: MacBook Air removed; MacBook remains.")
    print("Before Removal:", products_before)
    print("Removed Product: MacBook Air")
    print("Actual Remaining Products:", products_after)
    print("STATUS: PASS")
    print("========================================")


except AssertionError as error:
    # Save evidence if the expected result is not met.
    driver.save_screenshot(screenshot_file)

    print("\nSTATUS: FAIL")
    print("Reason:", error)
    raise


except Exception as error:
    # Save evidence if Selenium encounters an error.
    driver.save_screenshot(screenshot_file)

    print("\nSTATUS: ERROR")
    print("Error:", type(error).__name__, error)
    raise


finally:
    # Keep Chrome open for screenshots and inspection.
    print("\nTEST FINISHED - Chrome is still open.")
    print("Take screenshots for your assignment.")

    try:
        input("\nPress ENTER to close Chrome...")
    except EOFError:
        pass

    # Close Chrome when the tester is ready.
    driver.quit()

