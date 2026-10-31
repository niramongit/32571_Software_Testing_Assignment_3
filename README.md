# 32571 Software Testing – Assignment 3

**Member 1:** Niramon Kitrattanasak  
**Student ID:** 25459532  
**University:** University of Technology Sydney (UTS)  
**Website Under Test:** https://opencart.abstracta.us/

## 1. Project Overview

This repository contains nine automated test scripts developed using Python Selenium WebDriver with Google Chrome for Software Testing Assignment 3.

The testing covers three functions of the OpenCart demonstration website:

- **F1 – User Registration (T001)**
- **F5 – Product Search (T005)**
- **F9 – Product Comparison (T009)**

Each function includes three test scenarios. The scripts verify expected and actual results using assertions, display PASS, FAIL or ERROR in the terminal, and capture screenshots as testing evidence.

## 2. Test Scenarios and Results

### F1 – User Registration (T001)

| Scenario | Python Script | Result |
|---|---|---|
| TC01-S1: Valid Registration | test_registration.py | PASS |
| TC01-S2: Duplicate Email | test_duplicate_registration.py | PASS |
| TC01-S3: Invalid First Name | test_invalid_registration.py | PASS |

**Overall Result:** 3 Passed, 0 Failed.

### F5 – Product Search (T005)

| Scenario | Python Script | Result |
|---|---|---|
| TC02-S1: Full Product Name | test_product_search.py | PASS |
| TC02-S2: Partial Keyword | test_partial_product_search.py | PASS |
| TC02-S3: Nonexistent Product | test_no_product_results.py | FAIL |

**Overall Result:** 2 Passed, 1 Failed.

**Defect DEF-001:** When searching for a nonexistent product, the website displays "Your shopping cart is empty!" instead of a message indicating that no products match the search criteria.

### F9 – Product Comparison (T009)

| Scenario | Python Script | Result |
|---|---|---|
| TC03-S1: Compare Two Products | test_product_comparison.py | PASS |
| TC03-S2: Remove One Product | test_remove_comparison.py | PASS |
| TC03-S3: Remove All Products | test_empty_comparison.py | FAIL |

**Overall Result:** 2 Passed, 1 Failed.

**Defect DEF-002:** After removing all compared products, the website displays "Your shopping cart is empty!" instead of an appropriate product comparison message.

## 3. Overall Test Results

| Test Results | Total |
|---|---|
| Total Functions | 3 |
| Total Test Scenarios | 9 |
| Passed | 7 |
| Failed | 2 |
| Errors | 0 |

The two failed scenarios identified incorrect website messages. These results are based on the recorded test execution and screenshots.

## 4. Test Environment and Tools

- **Operating System:** macOS (Apple Silicon ARM64)
- **Programming Language:** Python 3.14.3
- **Automation Tool:** Selenium WebDriver 4.51.0
- **Web Browser:** Google Chrome 155.0.8059.85
- **Code Editor:** Visual Studio Code
- **HTML Inspection:** Chrome Developer Tools
- **Testing Approach:** Standalone Python Selenium scripts

## 5. Installation and Setup

**Step 1:** Install Python and Google Chrome.

**Step 2:** Download or clone this GitHub repository.

**Step 3:** Open the project folder in Visual Studio Code.

**Step 4:** Create and activate a Python virtual environment using the terminal.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Step 5:** Install Selenium WebDriver.

```bash
python -m pip install selenium
```

## 6. Running the Automated Tests

Open the VS Code terminal in the folder containing the Python scripts.

### F1 – User Registration

```bash
python test_registration.py
python test_duplicate_registration.py
python test_invalid_registration.py
```

Run `test_registration.py` before `test_duplicate_registration.py`, because the first script creates a unique registered email address and saves it to `F1_registered_email.txt`. The duplicate-registration script uses this email to test whether the website rejects an existing account.

### F5 – Product Search

```bash
python test_product_search.py
python test_partial_product_search.py
python test_no_product_results.py
```

### F9 – Product Comparison

```bash
python test_product_comparison.py
python test_remove_comparison.py
python test_empty_comparison.py
```

Each script runs an automated browser test, checks the actual website response, and displays the test status in the terminal.

Some scripts require pressing Enter in the terminal to close the Chrome browser after execution.

## 7. Screenshot Evidence

Screenshots were captured during test execution to demonstrate the website behaviour and support the recorded test results.

Example screenshot filenames:

- F1_TC01_S1_success.png
- F1_TC01_S2_duplicate_email.png
- F1_TC01_S3_invalid.png
- F5_TC02_S1_search.png
- F5_TC02_S2_partial_search.png
- F5_TC02_S3_Nonexistent_Product.png
- F9_TC03_S1_Compare_Two_Products.png
- F9_TC03_S2_Remove_One_Product.png
- F9_TC03_S3_Remove_All_Products.png

The screenshots are also included in the assignment report.

## 8. Conclusion

The automated testing covered three OpenCart functions using nine Python Selenium WebDriver test scenarios.

Seven scenarios passed and two scenarios failed because the website displayed incorrect messages for empty product search results and an empty product comparison list.

The testing demonstrated successful automated validation of user registration, product searching, and product comparison functionality while identifying two potential usability defects.

## 9. Notes

This repository contains Member 1's contribution to the group assignment. The complete group project covers 12 functions tested by four team members.

The scenario labels TC01, TC02 and TC03 are retained to match the current Python scripts and screenshot filenames.

The website is a public demonstration store, and its behaviour may change over time.
