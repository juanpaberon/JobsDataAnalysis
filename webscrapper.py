import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

# specifies the path to the chromedriver.exe
driver = webdriver.Chrome(r'C:\Users\juanp\Documents\chromedriver')
time.sleep(2)
driver.maximize_window()

# driver.get method() will navigate to a page given by the URL address
driver.get('https://www.linkedin.com/jobs/search/?f_E=2&f_TPR=r604800&f_WRA=true&geoId=103644278&keywords=(data%20scientist)AND(python)AND(git)&location=United%20States&sortBy=R')
time.sleep(10)

# Find the information about the date the job was posted, the name of the position, and location
bs = BeautifulSoup(driver.page_source, 'html.parser')

infos = []

for job in bs.findAll('ul',{'class':'jobs-search__results-list'})[0].findAll('li'):
    job_desc = list(job)[1]
    print('|----------|')
    try:
        print(job_desc.find('time',{'class':"job-search-card__listdate"}).attrs['datetime'])
        infos.append(job_desc.find('time',{'class':"job-search-card__listdate"}).attrs['datetime'])
    except:
        print(job_desc.find('time',{'class':"job-search-card__listdate--new"}).attrs['datetime'])
        infos.append(job_desc.find('time',{'class':"job-search-card__listdate--new"}).attrs['datetime'])


# Find the location of the links to expand the information
job_results = driver.find_element_by_class_name('jobs-search__results-list')
jobs = job_results.find_elements(By.CLASS_NAME,'base-card__full-link')

print(len(jobs))

# Clink on each job to access their description
for i, job in enumerate(jobs):
    print()
    for info in infos:
        print(info)
    print()
    job.click()
    time.sleep(1.5)
    driver.find_element_by_class_name('show-more-less-html__button').click()
    time.sleep(2)
#     bs = BeautifulSoup(driver.page_source, 'html.parser')
#     des = bs.findAll('div', {'class':'show-more-less-html__markup'})[0]
#     print(des)
#     print()
#     job_cri = bs.findAll('ul', {'class':'job-criteria__list'})[0]
#     print(job_cri)
#     print()
#     print('|---|')
#     print()