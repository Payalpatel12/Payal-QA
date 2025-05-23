

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
import secrets


---------CHROME DRIVER SETUP------------------------------

options = Options()
# options.add_argument("--headless")  # Uncomment to run headless
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)



try:
    driver.get("https://www.dutch.com/")
    time.sleep(3)

---------Start consultation----------------------------------
    driver.find_element(By.LINK_TEXT, "I NEED TO SEE A VET").click()
    time.sleep(3)



------------PET INFO FORM -------------------------------

# Select pet type - Dog (radio button)
dog_radio = driver.find_element(By.ID, "dog")
dog_radio.click()

# Enter pet's name
pet_name_input = driver.find_element(By.ID, "pet-name")
pet_name_input.send_keys("Milly")
print("Pet name entered successfully.")

# Select pet's home state (dropdown)
state_dropdown = Select(driver.find_element(By.ID, "state"))
state_dropdown.select_by_visible_text("California")
print("Successfully selected California from the dropdown.")

# Click the Continue button
continue_button = driver.find_element(By.XPATH, "//button[contains(text(),'Continue')]")
continue_button.click()
print("Pet Info form submitted successfully.")

# Wait for the next page to load
time.sleep(5)



----------PET HEALTH ISSUES---------------------------------------


checkbox_ids = ["Anxiety", "Coughing", "Weight"]

for checkbox_id in checkbox_ids:
    checkbox_element = driver.find_element(By.ID, checkbox_id)
    
    if not checkbox_element.is_selected():
        checkbox_element.click()
        print("Selected the issue: " + checkbox_id)
    else:
        print("Issue already selected: " + checkbox_id)

# Click the Continue button
continue_button = driver.find_element(By.XPATH, "//button[contains(text(),'Continue')]")
continue_button.click()
print("Pet Issue form submitted successfully.")

# Wait for the next page to load
time.sleep(5)


------------MODAL (POP UP)----------------------
note:  Wait for the modal to appear and Used XPath that combines the div class and the button's text (Continue). This allows me to specifically locate the button inside the modal. 
    
continue_button_modal = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='relative w-full space-y-6 rounded-lg bg-white p-6 text-center']//button[contains(text(),'Continue')]"))
    )

    # Click the "Continue" button inside the modal
    continue_button_modal.click()
    print("Clicked on 'Continue' in the modal.")

except TimeoutException:
    print("Timeout: 'Continue' button in the modal was not clickable within the time limit.")


----------------REGISTRATION-----------------------------------------------

email = wait.until(EC.presence_of_element_located((By.ID, "input_7")))
    email.send_keys(secrets.USERNAME)
    password = wait.until(EC.presence_of_element_located((By.ID, "input_8")))
    password.send_keys(secrets.PASSWORD)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Register') and @type='submit']").click()
    print("Registration submitted.")

--------------------PLAN SELECTIONS---------------------------------

 #  Verify the "Pick a plan for" header is present
    plan_header = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Pick a plan for')]")))
    assert "Pick a plan for" in plan_header.text
    print("Registration successful. Reached plan selection page.")

    # Select the 1-month plan radio button
    plan_option = wait.until(EC.element_to_be_clickable((By.ID, "product-6962656215216")))
    plan_option.click()
    print("Selected 1-month plan.")

    #  Click the "Continue with Monthly" button
    continue_button = wait.until(EC.element_to_be_clickable((By.ID, "register-plan-selection-cta")))
    continue_button.click()
    print("Proceeded with 1-month plan.")

except Exception as e:
    print("Error during plan selection or navigation check: " + str(e))

--------------------MODAL----------------Continue with Monthly---------------------------

 WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "modal-badge"))
    )

    # Wait for the "Continue with Monthly" button to be clickable
    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[contains(text(), 'Continue with Monthly')]"
        ))
    )

    # Click the button
    continue_button.click()
    print("Clicked on 'Continue with Monthly' button in the modal.")

except TimeoutException:
    print("Timeout: 'Continue with Monthly' button was not clickable in time.")


-------------------INSURANCE--------------------------------------------------

# Wait for the insurance header to appear
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//h1[contains(text(), 'Add accident insurance')]")
    ))
    print("Insurance page loaded successfully.")

    # Locate both buttons
    add_insurance_button = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//button[contains(text(), 'Add insurance')]")
    ))

    no_insurance_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(), 'No Insurance for my pet')]")
    ))

    print("Both 'Add insurance' and 'No Insurance for my pet' buttons are present.")

    # DECIDE TO GO WITH NO INSURANCA )
    no_insurance_button.click()
    print("Clicked on 'No Insurance for my pet' button.")

    # Confirm navigation to next page by checking logo
    logo = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//img[@alt='dutch-header-logo.png']")
    ))

    assert logo.is_displayed(), "Dutch logo is not displayed."
    print("Successfully reached checkout page — Dutch logo is visible.")

except Exception as e:
    print("Error during insurance selection or checkout validation: " + str(e))


---------------CHECKOUT PAGE-------------------------------------------------




 # Email verification
    email_element = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//div[contains(text(), '@') and contains(text(), '.com')]")
    ))
    displayed_email = email_element.text.strip()
    expected_email = secrets.USERNAME.strip().lower()
    actual_email = displayed_email.lower()

    assert actual_email == expected_email, f"Email mismatch. Expected: {expected_email}, Found: {actual_email}"
    print("Email is correctly pre-filled and matches: " + displayed_email)

    # Credit card section visibility
    credit_card_radio = wait.until(EC.visibility_of_element_located((By.ID, "basic-creditCards")))
    assert credit_card_radio is not None, "Credit Card payment option is not visible"
    print("Confirmed: Filling in credit card information.")

    # Card number
    card_input = wait.until(EC.visibility_of_element_located((By.ID, "number")))
    card_input.send_keys(secrets.CARD_NUMBER)
    digits = card_input.get_attribute("value").replace(" ", "")
    assert digits.isdigit(), "Card number must contain only digits"
    assert len(digits) <= 19, "Card number exceeds maximum length"
    print("Card number entered and validated: " + digits)

    # Expiry date
    expiry_input = wait.until(EC.visibility_of_element_located((By.ID, "expiry")))
    expiry_input.send_keys(secrets.EXPIRY)  # Format: "12 2025"
    entered_expiry = expiry_input.get_attribute("value").strip()
    assert " " in entered_expiry and len(entered_expiry) == 7, "Invalid expiry format"
    month, year = entered_expiry.split(" ")
    assert month.isdigit() and year.isdigit(), "Expiry must be numeric"
    assert 1 <= int(month) <= 12, "Month must be between 01 and 12"
    assert len(year) == 4, "Year must be in YYYY format"
    print("Expiry entered and validated: " + entered_expiry)

    # CVC
    cvc_input = wait.until(EC.visibility_of_element_located((By.ID, "verification_value")))
    cvc_input.send_keys(secrets.CVC)
    cvc_value = cvc_input.get_attribute("value").strip()
    assert cvc_value.isdigit(), "CVC must be numeric"
    assert 3 <= len(cvc_value) <= 4, "CVC must be 3 or 4 digits long"
    print("CVC entered and validated: " + cvc_value)

    # Name on card
    name_input = wait.until(EC.visibility_of_element_located((By.ID, "name")))
    name_input.send_keys(secrets.NAME_ON_CARD)
    actual_name = name_input.get_attribute("value").strip()
    assert actual_name == secrets.NAME_ON_CARD, f"Name mismatch: {actual_name}"
    print("Name on card entered correctly.")

    print("All fields validated successfully.")

except TimeoutException:
    print("Error: Timed out waiting for an element to appear.")

except AssertionError as ae:
    print("Validation failed: " + str(ae))

except Exception as e:
    print("Unexpected error during checkout: " + str(e))






-------------------BILLING ADDRESS ---------------------------------------


 # Country Dropdown
    country_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "Select20")))
    Select(country_dropdown).select_by_visible_text("United States")
    selected_country = Select(country_dropdown).first_selected_option.text
    assert selected_country == "United States", "Country selection failed"
    print("Country selected: United States")

    # First Name
    first_name_input = wait.until(EC.visibility_of_element_located((By.ID, "TextField43")))
    first_name_input.clear()
    first_name_input.send_keys(secrets.FIRST_NAME)
    assert first_name_input.get_attribute("value") == secrets.FIRST_NAME, "First name input failed"
    print("First name entered")

    # Last Name
    last_name_input = wait.until(EC.visibility_of_element_located((By.ID, "TextField44")))
    last_name_input.clear()
    last_name_input.send_keys(secrets.LAST_NAME)
    assert last_name_input.get_attribute("value") == secrets.LAST_NAME, "Last name input failed"
    print("Last name entered")

    # Address
    address_input = wait.until(EC.visibility_of_element_located((By.ID, "billing-address1")))
    address_input.clear()
    address_input.send_keys(secrets.ADDRESS)
    assert address_input.get_attribute("value") == secrets.ADDRESS, "Address input failed"
    print("Address entered")

    # Apartment
    apartment_input = wait.until(EC.visibility_of_element_located((By.ID, "TextField45")))
    apartment_input.clear()
    apartment_input.send_keys(secrets.APARTMENT)
    assert apartment_input.get_attribute("value") == secrets.APARTMENT, "Apartment input failed"
    print("Apartment entered")

    # City
    city_input = wait.until(EC.visibility_of_element_located((By.ID, "TextField46")))
    city_input.clear()
    city_input.send_keys(secrets.CITY)
    assert city_input.get_attribute("value") == secrets.CITY, "City input failed"
    print("City entered")

    # State Dropdown
    state_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "Select21")))
    Select(state_dropdown).select_by_visible_text(secrets.STATE)
    selected_state = Select(state_dropdown).first_selected_option.text
    assert selected_state == secrets.STATE, "State selection failed"
    print("State selected: " + secrets.STATE)

    # ZIP Code
    zip_input = wait.until(EC.presence_of_element_located((By.ID, "TextField47")))
    zip_input.clear()
    zip_input.send_keys(secrets.ZIP)
    assert zip_input.get_attribute("value") == secrets.ZIP, "ZIP code input failed"
    print("ZIP code entered")

    # Phone Number
    phone_input = wait.until(EC.presence_of_element_located((By.ID, "TextField48")))
    phone_input.clear()
    phone_input.send_keys(secrets.PHONE)
    assert phone_input.get_attribute("value") == secrets.PHONE, "Phone number input failed"
    print("Phone number entered")

    print("Billing address completed and verified successfully.")

except Exception as e:
    print("Billing form error: " + str(e))































