import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import random

# Path to your chromedriver executable
chrome_driver_path = '../chromedriver/chromedriver.exe'

# Initialize the driver with options to handle special characters and SSL errors
chrome_options = Options()
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')

service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to apply for a job
def apply_for_job():
    job_url = 'https://www.linkedin.com/jobs/view/3921132987/?alternateChannel=search&refId=Tg1lqkjnwdCnczjJFX8a4A%3D%3D&trackingId=puyc4jpDMC84xzn9DP2JUQ%3D%3D'
    print(f"Navigating to job URL: {job_url}")
    driver.get(job_url)
    time.sleep(random.uniform(3, 6))  # Random delay between 3 and 6 seconds

    try:
        # Click the "Easy Apply" button
        easy_apply_button = driver.find_element(By.XPATH, "//button[contains(text(),'Easy Apply')]")
        easy_apply_button.click()
        time.sleep(random.uniform(2, 5))  # Random delay between 2 and 5 seconds

        # Fill in the application form
        driver.find_element(By.ID, 'first-name').send_keys('FirstName')
        time.sleep(random.uniform(1, 3))  # Random delay between 1 and 3 seconds
        driver.find_element(By.ID, 'last-name').send_keys('LastName')
        time.sleep(random.uniform(1, 3))
        driver.find_element(By.ID, 'phone-number').send_keys('PhoneNumber')
        time.sleep(random.uniform(1, 3))
        driver.find_element(By.ID, 'email-address').send_keys('Email')
        time.sleep(random.uniform(1, 3))

        # Click the "Next" button
        next_button = driver.find_element(By.XPATH, "//button[contains(text(),'Next')]")
        next_button.click()
        time.sleep(random.uniform(2, 5))

        # Upload the resume
        resume_path = 'path/to/resume.pdf'
        print(f"Uploading resume from: {resume_path}")
        resume_upload_button = driver.find_element(By.ID, 'upload-resume')
        resume_upload_button.send_keys(resume_path)
        time.sleep(random.uniform(3, 6))

        # Click the "Next" button again
        next_button = driver.find_element(By.XPATH, "//button[contains(text(),'Next')]")
        next_button.click()
        time.sleep(random.uniform(2, 5))

        # Click the "Submit" button
        submit_button = driver.find_element(By.XPATH, "//button[contains(text(),'Submit')]")
        submit_button.click()
        time.sleep(random.uniform(3, 6))
    except Exception as e:
        print(f"Error applying for job at {job_url}: {e}")

# Main execution
if __name__ == "__main__":
    apply_for_job()
    driver.quit()