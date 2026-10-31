
# Assignment 3 - Software Testing
# Tester: Niramon Kitrattanasak
# Test Case ID: T001
# Function: F1 - User Registration
# Scenario 1 (TC01-S1): Register with Valid Information
# Tool: Python + Selenium WebDriver

import uuid
from pathlib import Path
from urllib.parse import unquote

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Generate a unique email address for each test run.
test_email = f"niramon.{uuid.uuid4().hex[:10]}@example.com"
test_password = "Testing2026!Secure"

# Step 1: Open Google Chrome using Selenium WebDriver.
driver = webdriver.Chrome()
driver.maximize_window()
driver.set_page_load_timeout(45)

try:
    # Open the registration page on the new website.
    driver.get(
        "https://opencart.abstracta.us/"
        "index.php?route=account/register"
    )

    # Step 2: Wait until the registration form is ready.
    wait = WebDriverWait(driver, 30)

    wait.until(
        EC.visibility_of_element_located(
            (By.ID, "input-firstname")
        )
    )

    # Step 3: Enter valid personal details.
    driver.find_element(
        By.ID, "input-firstname"
    ).send_keys("Niramon")

    driver.find_element(
        By.ID, "input-lastname"
    ).send_keys("TestUser")

    driver.find_element(
        By.ID, "input-email"
    ).send_keys(test_email)

    driver.find_element(
        By.ID, "input-telephone"
    ).send_keys("0400123456")

    # Step 4: Enter and confirm the password.
    driver.find_element(
        By.ID, "input-password"
    ).send_keys(test_password)

    driver.find_element(
        By.ID, "input-confirm"
    ).send_keys(test_password)

    # Step 5: Accept the Privacy Policy.
    checkbox = driver.find_element(
        By.NAME, "agree"
    )

    if not checkbox.is_selected():
        driver.execute_script(
            "arguments[0].click();", checkbox
        )

    # Click Continue to submit the registration form.
    wait.until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                'input[type="submit"][value="Continue"], '
                'button[type="submit"]'
            )
        )
    ).click()

    # Step 6: Check whether registration was successful.
    # The URL may contain "/" or its encoded form "%2F".
    wait.until(
        lambda d: (
            "account/success" in unquote(d.current_url)
            or any(
                element.is_displayed() and element.text.strip()
                for element in d.find_elements(
                    By.CSS_SELECTOR,
                    ".alert-danger, .text-danger"
                )
            )
        )
    )

    # Verify that the account success page was reached.
    assert "account/success" in unquote(driver.current_url), (
        "Registration did not reach the success page."
    )

    
    # Verify that the account confirmation message appears.
    content = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "content")
        )
    )

    # Expected message on the new OpenCart website.
    expected_message = (
        "your new account has been successfully created"
    )

    # Find the actual confirmation message on the page.
    matching_messages = [
        line.strip()
        for line in content.text.splitlines()
        if expected_message in line.lower()
    ]

    # Verify that the confirmation message was displayed.
    assert matching_messages, (
        "Registration success message was not found."
    )

    actual_message = matching_messages[0]



    # Step 7: Save a screenshot for the assignment.
    driver.save_screenshot(
        "F1_TC01_S1_success.png"
    )

    # Save the email for the duplicate-registration test.
    Path("F1_registered_email.txt").write_text(
        test_email,
        encoding="utf-8"
    )

    # Display the test results in the terminal.
    print("\n========================================")
    print("Tester: Niramon Kitrattanasak")
    print("Test Case: T001")
    print("Function: F1 - User Registration")
    print("Scenario: TC01-S1 - Valid Registration")
    print("----------------------------------------")
    print("Expected: Account created successfully.")
    print("Actual:", actual_message)
    print("Test Email:", test_email)
    print("STATUS: PASS")
    print("========================================")


except AssertionError as error:
    # Save evidence if the expected result is not met.
    driver.save_screenshot(
        "F1_TC01_S1_fail.png"
    )

    print("\nSTATUS: FAIL")
    print("Reason:", error)
    raise


except Exception as error:
    # Save evidence if Selenium encounters an error.
    driver.save_screenshot(
        "F1_TC01_S1_error.png"
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
