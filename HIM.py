import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

def playAI():

    # Setup Chrome options
    chrome_options = webdriver.ChromeOptions()

    #keeps the tab open
    chrome_options.add_experimental_option("detach", True)

    # chrome_options.add_argument("--headless")  # Uncomment this if you want to run headless

    # Setup the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Get the absolute path to your HTML file
    html_path = os.path.abspath("test.html")

    # Navigate to the page using the file:// protocol
    driver.get(f"file://{html_path}")


    iframe = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "play-ai-embed"))
    )

    print(f"Iframe found: ID = {iframe.get_attribute('id')}, Src = {iframe.get_attribute('src')}")

    # Switch to the iframe
    driver.switch_to.frame(iframe)

    # Wait for the iframe content to load (adjust timeout as needed)
    time.sleep(4)
        
    try:
        # Try to find a clickable element within the iframe
        clickable = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button, a, [role='button']"))
        )
        clickable.click()
        print("Clicked on a clickable element within the iframe")

        input()

        driver.refresh()

    except Exception as e:
        print(f"An error occurred: {e}")
        # Take a screenshot for debugging
        driver.save_screenshot("error_screenshot.png")
        print("Screenshot saved as error_screenshot.png")