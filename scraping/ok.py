# Import required packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import shutil

# Automatically install correct ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Base URL
page_URL = "https://leetcode.com/problemset/all/?page="

# Function to scrape links
def get_a_tags(url):
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "a"))
    )
    
    links = driver.find_elements(By.TAG_NAME, "a")
    ans = [i.get_attribute("href") for i in links if i.get_attribute("href") and "/problems/" in i.get_attribute("href")]
    
    return list(set(ans))

# Scrape pages
my_ans = []
for i in range(1, 55):
    my_ans += get_a_tags(page_URL + str(i))

# Remove duplicates
my_ans = list(set(my_ans))

# Ensure scraping folder exists
if not os.path.exists("scraping"):
    os.makedirs("scraping")

# Save links to lc.txt
with open("scraping/lc.txt", 'w') as f:
    for j in my_ans:
        f.write(j + '\n')

print(f"Total unique links found: {len(my_ans)}")

# Function to remove /solution links
def remove_solution_lines(input_file):
    temp_file = input_file + ".tmp"
    
    with open(input_file, 'r') as file, open(temp_file, 'w') as temp:
        for line in file:
            if "/solution" not in line:
                temp.write(line)

    shutil.move(temp_file, input_file)

remove_solution_lines("scraping/lc.txt")

# Close browser
driver.quit()
