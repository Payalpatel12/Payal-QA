from pages.home_page import HomePage
from pages.pet_info_page import PetInfoPage
from pages.pet_issues_page import PetIssuesPage
from pages.registration_page import RegistrationPage
from pages.checkout_page import CheckoutPage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.dutch.com/")

HomePage(driver).start_consultation()
PetInfoPage(driver).fill_pet_info()
PetIssuesPage(driver).select_issues()
RegistrationPage(driver).register_and_select_plan()
CheckoutPage(driver).complete_checkout()
