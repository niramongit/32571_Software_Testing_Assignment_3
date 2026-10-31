
# Assignment 3 - Software Testing
# Tester: Niramon Kitrattanasak
# Test Case ID: T005
# Function: F5 - Product Search
# Scenario 3 (TC02-S3): Search for a Product That Does Not Exist
# Tool: Python + Selenium WebDriver

from urllib.parse import parse_qs, urlsplit

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Product keyword used for testing.
search_keyword = "xyznonexistent98765"

# Screenshot evidence for TC02-S3: Nonexistent Product.
screenshot_file = "F5_TC02_S3_Nonexistent_Product.png"


# Step 1: Open Google Chrome using Selenium WebDriver.
driver = webdriver.Chrome()
driver.maximize_window()
driver.set_page_load_timeout(45)

try:
    # Open the OpenCart website.
    driver.get("https://opencart.abstracta.us/")

    # Step 2: Wait for the search field to become available.
    wait = WebDriverWait(driver, 30)

    search_box = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "#search input[name='search']")
        )
    )

    # Step 3: Enter a nonexistent product keyword.
    search_box.clear()
    search_box.send_keys(search_keyword)

    # Step 4: Press Enter to submit the search.
    search_box.send_keys(Keys.ENTER)

    # Step 5: Wait until the search results page is ready.
    wait.until(
        lambda d: (
            parse_qs(
                urlsplit(d.current_url).query
            ).get("route", [""])[0] == "product/search"
        )
    )

    content = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "content")
        )
    )

    # Read the current URL and search parameters.
    current_url = driver.current_url
    query = parse_qs(urlsplit(current_url).query)

    actual_keyword = query.get("search", [""])[0]

    # Read the text displayed on the results page.
    page_text = " ".join(content.text.split())

    # Find any product cards displayed in the results.
    product_cards = driver.find_elements(
        By.CSS_SELECTOR,
        "#content .product-layout, "
        "#content .product-thumb"
    )

    # Locate the expected no-results message.
    expected_message = (
        "There is no product that matches "
        "the search criteria."
    )

    no_results_displayed = (
        expected_message.lower() in page_text.lower()
    )

    # Display information for checking and debugging.
    print("\n========================================")
    print("Tester: Niramon Kitrattanasak")
    print("Test Case: T005")
    print("Function: F5 - Product Search")
    print("Scenario: TC02-S3 - Nonexistent Product")
    print("----------------------------------------")
    print("Search Keyword:", search_keyword)
    print("Website URL:", current_url)
    print("Actual Search Keyword:", actual_keyword)
    print("Product Cards Found:", len(product_cards))
    print("No-Results Message Found:", no_results_displayed)
    print("Page Text:", page_text[:600])

    # Step 6: Verify the expected results.
    assert actual_keyword == search_keyword, (
        "The search keyword was not submitted correctly."
    )

    assert len(product_cards) == 0, (
        "Products were displayed for a nonexistent keyword."
    )

    assert no_results_displayed, (
    "Expected a message explaining that no products "
    "matched the search criteria. "
    f"Actual page content: {page_text[:300]}"
)

    # Step 7: Save screenshot evidence.
    driver.save_screenshot(screenshot_file)

    # Display the final test result.
    print("----------------------------------------")
    print("Expected: No matching products message appears.")
    print("Actual:", expected_message)
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
    print("Current URL:", driver.current_url)
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
