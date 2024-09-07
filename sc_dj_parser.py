import re
import openpyxl
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Function to find email in user description
def find_email(text):
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    email_alt_pattern = r'[a-zA-Z0-9_.+-]+\[at\][a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    email = re.search(email_pattern, text) or re.search(email_alt_pattern, text)
    return email.group(0) if email else None

# Function to save data to an Excel file
def save_to_excel(data, filename="user_data.xlsx"):
    try:
        workbook = openpyxl.load_workbook(filename)
        sheet = workbook.active
    except FileNotFoundError:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(["User URL", "User Name", "Email"])
    
    for row in data:
        sheet.append(row)
    workbook.save(filename)

# Function to scroll through the page and collect all user links
def collect_user_links(driver, scroll_pause_time=2):
    user_links = []
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        new_links = [link.get_attribute("href") for link in driver.find_elements(By.CLASS_NAME, 'userBadgeListItem__image')]
        user_links.extend(new_links)
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    return list(set(user_links))  # Remove duplicates

# Function to process each user page and collect necessary data
def process_user_pages(driver, user_links, batch_size, soundcloud_channel):
    data_batch = []
    
    for idx, user_url in enumerate(user_links):
        try:
            driver.get(user_url)
            
            # Wait for the username to be present
            user_name_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'profileHeaderInfo__userName'))
            )
            user_name = user_name_element.text.lower()
            
            # Get user description
            description_element = driver.find_element(By.CLASS_NAME, 'truncatedUserDescription__content')
            description_text = description_element.text.lower()
            
            # Check if 'dj' is in username or description
            if 'dj' in user_name or 'dj' in description_text:
                email = find_email(description_text)
                
                if email:
                    data_batch.append([user_url, user_name, email])
        
        except Exception:
            print(f"Error on page {user_url}")
        
        if (idx + 1) % batch_size == 0 and data_batch:
            save_to_excel(data_batch, f'{soundcloud_channel}.xlsx')
            data_batch = []
    
    if data_batch:
        save_to_excel(data_batch, f'{soundcloud_channel}.xlsx')

# Main function to control the flow of the script
def main(soundcloud_channel):
    driver = webdriver.Chrome()
    driver.get(f'https://soundcloud.com/{soundcloud_channel}/followers')
    
    user_links = collect_user_links(driver)
    process_user_pages(driver, user_links, batch_size=10, soundcloud_channel=soundcloud_channel)
    
    driver.quit()

# Entry point for the script using argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SoundCloud DJ parser")
    parser.add_argument('--name', type=str, help='SoundCloud channel name (e.g., "bcco")')
    args = parser.parse_args()
    
    if args.name:
        soundcloud_channel = args.name
    else:
        soundcloud_channel = input("Enter the SoundCloud channel name: ")
    
    main(soundcloud_channel)
