
# Assignment 3 - Software Testing
# Tester: Niramon Kitrattanasak
# Test Case ID: T001
# Function: F1 - User Registration
# Scenario 2 (TC01-S2): Register with an Existing Email Address
# Tool: Python + Selenium WebDriver

from pathlib import Path
from urllib.parse import unquote

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Read the registered email from Scenario 1.
email_file = Path(__file__).with_name("F1_registered_email.txt")

if not email_file.exists():
    raise FileNotFoundError(
        "Run test_registration.py first to create the test email."
    )

test_email = email_file.read_text(encoding="utf-8").strip()
test_password = "Testing2026!Secure"

assert test_email, "The registered email file is empty."


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

    # Step 2: Wait for the registration form.
    wait = WebDriverWait(driver, 30)

    wait.until(
        EC.visibility_of_element_located(
            (By.ID, "input-firstname")
        )
    )

    # Step 3: Enter valid details with an existing email.
    driver.find_element(
        By.ID, "input-firstname"
    ).send_keys("Niramon")

    driver.find_element(
        By.ID, "input-lastname"
    ).send_keys("DuplicateTest")

    driver.find_element(
        By.ID, "input-email"
    ).send_keys(test_email)

    driver.find_element(
        By.ID, "input-telephone"
    ).send_keys("0400123456")

    # Step 4: Complete the password fields.
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

    # Step 5: Click Continue to submit registration.
    wait.until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                'input[type="submit"][value="Continue"], '
                'button[type="submit"]'
            )
        )
    ).click()

    # Step 6: Wait for the website's response.
    def registration_response(browser):

        # Detect if an account was unexpectedly created.
        if "account/success" in unquote(browser.current_url):
            return "SUCCESS_PAGE"

        # Find a visible warning message.
        warnings = browser.find_elements(
            By.CSS_SELECTOR, ".alert-danger"
        )

        for warning in warnings:
            if warning.is_displayed() and warning.text.strip():
                return warning.text.strip()

        return False

    response = wait.until(registration_response)

    # Verify the website did not create another account.
    assert response != "SUCCESS_PAGE", (
        "The website unexpectedly accepted a duplicate email."
    )

    # Verify the correct duplicate-email warning.
    assert "already registered" in response.lower(), (
        f"Unexpected registration warning: {response}"
    )

    # Step 7: Save screenshot evidence.
    driver.save_screenshot(
        "F1_TC01_S2_duplicate_email.png"
    )

    # Display the test results.
    print("\n========================================")
    print("Tester: Niramon Kitrattanasak")
    print("Test Case: T001")
    print("Function: F1 - User Registration")
    print("Scenario: TC01-S2 - Existing Email")
    print("----------------------------------------")
    print("Expected: Duplicate email is rejected.")
    print("Actual:", response)
    print("Test Email:", test_email)
    print("STATUS: PASS")
    print("========================================")


except AssertionError as error:
    # Save evidence when the expected result is not met.
    driver.save_screenshot(
        "F1_TC01_S2_fail.png"
    )

    print("\nSTATUS: FAIL")
    print("Reason:", error)
    raise


except Exception as error:
    # Save evidence if Selenium encounters an error.
    driver.save_screenshot(
        "F1_TC01_S2_error.png"
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
