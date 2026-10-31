
# Assignment 3 - Software Testing
# Tester: Niramon Kitrattanasak
# Test Case ID: T001
# Function: F1 - User Registration
# Scenario 3 (TC01-S3): Register with an Invalid First Name
# Tool: Python + Selenium WebDriver

import uuid
from urllib.parse import unquote

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Generate a unique email for the test.
test_email = f"niramon.invalid.{uuid.uuid4().hex[:10]}@example.com"
test_password = "Testing2026!Secure"


# Step 1: Open Google Chrome using Selenium WebDriver.
driver = webdriver.Chrome()
driver.maximize_window()
driver.set_page_load_timeout(45)

try:
    # Open the registration page.
    driver.get(
        "https://opencart.abstracta.us/"
        "index.php?route=account/register"
    )

    # Step 2: Wait for the registration form to be ready.
    wait = WebDriverWait(driver, 30)

    wait.until(
        EC.visibility_of_element_located(
            (By.ID, "input-firstname")
        )
    )

    # Step 3: Leave First Name empty (invalid input).
    driver.find_element(
        By.ID, "input-firstname"
    ).clear()

    # Step 4: Enter valid information in all other fields.
    driver.find_element(
        By.ID, "input-lastname"
    ).send_keys("TestUser")

    driver.find_element(
        By.ID, "input-email"
    ).send_keys(test_email)

    driver.find_element(
        By.ID, "input-telephone"
    ).send_keys("0400123456")

    driver.find_element(
        By.ID, "input-password"
    ).send_keys(test_password)

    driver.find_element(
        By.ID, "input-confirm"
    ).send_keys(test_password)

    # Accept the Privacy Policy.
    checkbox = driver.find_element(By.NAME, "agree")

    if not checkbox.is_selected():
        driver.execute_script(
            "arguments[0].click();", checkbox
        )

    # Step 5: Submit the registration form.
    wait.until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                'input[type="submit"][value="Continue"], '
                'button[type="submit"]'
            )
        )
    ).click()

    # Step 6: Check that the website rejects the invalid name.
    def registration_response(browser):

        # Detect unexpected successful registration.
        if "account/success" in unquote(browser.current_url):
            return ("SUCCESS_PAGE", "")

        # Look for a visible First Name validation error.
        errors = browser.find_elements(
            By.CSS_SELECTOR,
            "#content .text-danger, "
            "#content .invalid-feedback"
        )

        for error in errors:
            if (
                error.is_displayed()
                and "first name" in error.text.lower()
            ):
                return ("FIRST_NAME_ERROR", error.text.strip())

        return False

    response = wait.until(registration_response)

    # Verify that registration was rejected.
    assert response[0] == "FIRST_NAME_ERROR", (
        "Registration was not rejected for the invalid First Name."
    )

    actual_message = response[1]

    # Step 7: Save screenshot evidence.
    driver.save_screenshot(
        "F1_TC01_S3_invalid.png"
    )

    # Display the test results in the terminal.
    print("\n========================================")
    print("Tester: Niramon Kitrattanasak")
    print("Test Case: T001")
    print("Function: F1 - User Registration")
    print("Scenario: TC01-S3 - Invalid First Name")
    print("----------------------------------------")
    print("Expected: Invalid First Name is rejected.")
    print("Actual:", actual_message)
    print("Test Email:", test_email)
    print("STATUS: PASS")
    print("========================================")


except AssertionError as error:
    # Save evidence when the expected result is not met.
    driver.save_screenshot(
        "F1_TC01_S3_fail.png"
    )

    print("\nSTATUS: FAIL")
    print("Reason:", error)
    raise


except Exception as error:
    # Save evidence if Selenium encounters an error.
    driver.save_screenshot(
        "F1_TC01_S3_error.png"
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
