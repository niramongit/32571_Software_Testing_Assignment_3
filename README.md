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

## 3. Overall Test
