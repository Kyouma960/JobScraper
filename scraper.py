from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import csv

# Setup the webdriver (specify the path to your chromedriver)
driver = webdriver.Chrome(executable_path="/path/to/chromedriver")

# Open the website page that lists job posts (Replace with the actual URL)
driver.get('https://www.onlinejobs.ph')

# Give time for the page to load completely
time.sleep(5)

# Find all job postings on the page
job_listings = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/jobseekers/job/"]')

# List to hold all job data
job_data_list = []

# Loop through each job listing element to extract relevant information
for job_listing in job_listings:
    job_data = {}
    
    # Extract the job post URL
    try:
        job_data['Job post url'] = job_listing.get_attribute('href')
    except NoSuchElementException:
        job_data['Job post url'] = "N/A"
    
    # Extract the job title
    try:
        job_data['Title'] = job_listing.find_element(By.CSS_SELECTOR, 'h4.fs-16.fw-700').text
    except NoSuchElementException:
        job_data['Title'] = "N/A"
    
    # Extract the time of the job (e.g., Full Time or Part Time)
    try:
        job_data['Time of job'] = job_listing.find_element(By.CSS_SELECTOR, 'span.badge').text
    except NoSuchElementException:
        job_data['Time of job'] = "N/A"
    
    # Extract the date posted
    try:
        job_data['Date posted'] = job_listing.find_element(By.CSS_SELECTOR, 'p.fs-13.mb-0 em').text
    except NoSuchElementException:
        job_data['Date posted'] = "N/A"
    
    # Extract the salary
    try:
        job_data['Salary'] = job_listing.find_element(By.CSS_SELECTOR, 'dd.col').text
    except NoSuchElementException:
        job_data['Salary'] = "N/A"
    
    # Extract the job description
    try:
        job_data['Description'] = job_listing.find_element(By.CSS_SELECTOR, 'div.desc').text
    except NoSuchElementException:
        job_data['Description'] = "N/A"
    
    # Extract the "posted by" information
    try:
        posted_by = ""
        h4_elements = job_listing.find_elements(By.CSS_SELECTOR, 'h4.fs-16.fw-700')
        for h4_element in h4_elements:
            if "Posted on" not in h4_element.text:  # Skip the "Posted on" line
                posted_by = job_listing.find_element(By.CSS_SELECTOR, 'p.fs-13.mb-0').text.split('•')[0].strip()
                break
        job_data['Posted by'] = posted_by if posted_by else "N/A"
    except NoSuchElementException:
        job_data['Posted by'] = "N/A"
    
    # Add the job data to the list
    job_data_list.append(job_data)

# Close the driver after scraping
driver.quit()

# Save the job data to a CSV file
csv_file = 'job_listings.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Job post url', 'Title', 'Time of job', 'Date posted', 'Salary', 'Description', 'Posted by'])
    writer.writeheader()
    writer.writerows(job_data_list)

print(f'Job listings have been scraped and saved to {csv_file}')
