
# Assignment 3 - Software Testing
# Tester: Niramon Kitrattanasak
# Test Case ID: T009
# Function: F9 - Product Comparison
# Scenario 1 (TC03-S1): Compare Two Different Products
# Tool: Python + Selenium WebDriver

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Products used for testing.
product_names = ["MacBook", "MacBook Air"]

# Screenshot evidence for this scenario.
screenshot_file = "F9_TC03_S1_Compare_Two_Products.png"


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

    # Step 2: Wait for the product search results.
    wait = WebDriverWait(driver, 30)

    wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "#content .product-layout")
        )
    )

    # Function to add a selected product to comparison.
    def add_to_comparison(product_name, expected_count):

        # Find the product cards on the search results page.
        cards = driver.find_elements(
            By.CSS_SELECTOR,
            "#content .product-layout"
        )

        for card in cards:

            # Read the product name from the card.
            titles = card.find_elements(
                By.CSS_SELECTOR, "h4 a"
            )

            if not titles:
                continue

            if titles[0].text.strip() != product_name:
                continue

            # Find the Compare button for this product.
            buttons = card.find_elements(
                By.CSS_SELECTOR,
                'button[onclick*="compare.add"]'
            )

            assert buttons, (
                f"Compare button not found for {product_name}"
            )

            compare_button = buttons[0]

            # Scroll to the button and move the mouse over it.
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                compare_button
            )

            ActionChains(driver).move_to_element(
                compare_button
            ).perform()

            # Click the Compare button.
            compare_button.click()

            # Wait for the comparison counter to update.
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

    # Step 3: Add MacBook to the comparison list.
    add_to_comparison("MacBook", 1)

    # Step 4: Add MacBook Air to the comparison list.
    add_to_comparison("MacBook Air", 2)

    # Step 5: Open the Product Comparison page.
    driver.get(
        "https://opencart.abstracta.us/"
        "index.php?route=product/compare"
    )

    # Wait for the comparison table to appear.
    wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "#content table")
        )
    )

    # Step 6: Verify that both products appear separately.
    # Find the row labelled "Product".
    product_row = wait.until(
        lambda d: d.find_elements(
            By.XPATH,
            "//div[@id='content']//table//tr"
            "[td[1][normalize-space()='Product']]"
        )
    )[0]

    product_cells = product_row.find_elements(
        By.XPATH, "./td"
    )

    # Exclude the first cell containing the label "Product".
    actual_products = [
        cell.text.strip()
        for cell in product_cells[1:]
    ]

    # Verify that both products are in separate columns.
    assert (
        len(actual_products) == 2
        and set(actual_products) == set(product_names)
    ), (
        f"Unexpected comparison products: {actual_products}"
    )

    # Check that prices are displayed for both products.
    price_rows = driver.find_elements(
        By.XPATH,
        "//div[@id='content']//table//tr"
        "[td[1][normalize-space()='Price']]"
    )

    assert price_rows, "Price row was not found."

    price_cells = price_rows[0].find_elements(
        By.XPATH, "./td"
    )

    actual_prices = [
        cell.text.strip()
        for cell in price_cells[1:]
    ]

    assert (
        len(actual_prices) == 2
        and all(actual_prices)
    ), (
        f"Prices are missing: {actual_prices}"
    )

    # Step 7: Save screenshot evidence.
    driver.execute_script("window.scrollTo(0, 0);")

    driver.save_screenshot(screenshot_file)

    # Display test results in the terminal.
    print("\n========================================")
    print("Tester: Niramon Kitrattanasak")
    print("Test Case: T009")
    print("Function: F9 - Product Comparison")
    print("Scenario: TC03-S1 - Compare Two Different Products")
    print("----------------------------------------")
    print("Expected: Both products appear in separate columns.")
    print("Actual Products:", actual_products)
    print("Actual Prices:", actual_prices)
    print("STATUS: PASS")
    print("========================================")


except AssertionError as error:
    # Save screenshot if the expected result is not met.
    driver.save_screenshot(screenshot_file)

    print("\nSTATUS: FAIL")
    print("Reason:", error)
    raise


except Exception as error:
    # Save screenshot if Selenium encounters an error.
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
