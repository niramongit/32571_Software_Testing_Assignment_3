
# Assignment 3 - Software Testing
# Tester: Niramon Kitrattanasak
# Test Case ID: T005
# Function: F5 - Product Search
# Scenario 1 (TC02-S1): Search Using a Full Product Name
# Tool: Python + Selenium WebDriver

from urllib.parse import parse_qs, urlsplit

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Product keyword used for testing.
search_keyword = "MacBook"


# Step 1: Open Google Chrome using Selenium WebDriver.
driver = webdriver.Chrome()
driver.maximize_window()
driver.set_page_load_timeout(45)

try:
    # Open the new OpenCart website.
    driver.get("https://opencart.abstracta.us/")

    # Step 2: Wait for the search field to become available.
    wait = WebDriverWait(driver, 30)

    search_box = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "#search input[name='search']")
        )
    )

    # Step 3: Enter the full product name.
    search_box.clear()
    search_box.send_keys(search_keyword)

    # Step 4: Press Enter to search for the product.
    search_box.send_keys(Keys.ENTER)

    # Step 5: Wait for the search results page.
    def search_results_ready(browser):

        # Read the website's current route.
        query = parse_qs(urlsplit(browser.current_url).query)
        route = query.get("route", [""])[0]

        if route != "product/search":
            return False

        # Find product names from the results section.
        products = browser.find_elements(
            By.CSS_SELECTOR,
            "#content .product-layout h4 a, "
            "#content .product-thumb h4 a"
        )

        product_names = list(dict.fromkeys(
            product.text.strip()
            for product in products
            if product.is_displayed()
            and product.text.strip()
        ))

        # Check whether the website displays no results.
        page_text = browser.find_element(
            By.ID, "content"
        ).text.lower()

        no_results = (
            "there is no product that matches" in page_text
        )

        if product_names or no_results:
            return product_names

        return False

    product_names = wait.until(search_results_ready)

    # Step 6: Verify that matching products appear.
    matching_products = [
        name for name in product_names
        if search_keyword.lower() in name.lower()
    ]

    assert matching_products, (
        f"No products matched '{search_keyword}'. "
        f"Displayed products: {product_names}"
    )

    # Step 7: Save screenshot evidence.
    driver.save_screenshot(
        "F5_TC02_S1_search.png"
    )

    # Display test results in the terminal.
    print("\n========================================")
    print("Tester: Niramon Kitrattanasak")
    print("Test Case: T005")
    print("Function: F5 - Product Search")
    print("Scenario: TC02-S1 - Full Product Name")
    print("----------------------------------------")
    print("Expected: Products matching MacBook appear.")
    print("Actual: Matching products:", matching_products)
    print("Search Keyword:", search_keyword)
    print("STATUS: PASS")
    print("========================================")


except AssertionError as error:
    # Save evidence when the expected result is not met.
    driver.save_screenshot(
        "F5_TC02_S1_fail.png"
    )

    print("\nSTATUS: FAIL")
    print("Reason:", error)
    raise


except Exception as error:
    # Save evidence if Selenium encounters an error.
    driver.save_screenshot(
        "F5_TC02_S1_error.png"
    )

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
