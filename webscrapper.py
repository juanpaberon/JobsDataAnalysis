import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


def load_credentials():
    with open('credentials.txt') as f:
        lines = f.readlines()
    username, password = [l.strip() for l in lines]
    return username, password


def log_in(driver):
    username, password = load_credentials()

    username_field = driver.find_element_by_id('session_key')
    username_field.clear()
    username_field.send_keys(username)
    password_field = driver.find_element_by_id('session_password')
    password_field.clear()
    password_field.send_keys(password)

    time.sleep(1)

    submit_button = driver.find_element_by_class_name('sign-in-form__submit-button')
    submit_button.click()

    time.sleep(15)
    
    
def get_total_jobs(driver):
    # Find the information about the date the job was posted, the name of the position, and location
    bs = BeautifulSoup(driver.page_source, 'html.parser')
    return int(bs.find('small',{'class':'display-flex t-12 t-black--light t-normal'}).getText().strip().split(' ')[0])


def set_up_job_search(driver):
    driver_tmp = driver.find_element_by_class_name("application-outlet")
    driver_tmp = driver_tmp.find_element_by_class_name('job-search-ext')
    driver_tmp = driver_tmp.find_element_by_class_name('jobs-search-two-pane__wrapper')
    driver_tmp = driver_tmp.find_element_by_class_name('jobs-search-two-pane__results')
    driver_tmp = driver_tmp.find_element_by_css_selector(".jobs-search-results.display-flex.flex-column")
    return driver_tmp.find_elements_by_css_selector(".jobs-search-results__list-item.occludable-update.p0.relative.ember-view")


def get_job_info(driver, job):
    driver_tmp = driver.find_element_by_class_name("jobs-unified-top-card__content--two-pane")
    title = driver_tmp.find_element_by_css_selector(".t-24.t-bold").text
    company = driver_tmp.find_element_by_css_selector(".ember-view.t-black.t-normal").text
    location = driver_tmp.find_element_by_class_name("jobs-unified-top-card__bullet").text
    description = driver.find_element_by_css_selector(".jobs-description__container.m4").text
    return title, company, location, description


# specifies the path to the chromedriver.exe
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(r'C:\Users\juanp\Documents\chromedriver', chrome_options=options)

time.sleep(2)
driver.maximize_window()

driver.get("https://www.linkedin.com/")

current_job = 1

log_in(driver)

driver.get('https://www.linkedin.com/jobs/search/?f_E=2&f_TPR=r604800&f_WRA=true&geoId=103644278&keywords=(data%20scientist)AND(python)AND(git)&location=United%20States&sortBy=DD&start=0')
time.sleep(5)
total_jobs = get_total_jobs(driver)

jobs = set_up_job_search(driver)

for i, job in enumerate(jobs):
    print()
    job.click()
    time.sleep(1.5)
    title, company, location, description = get_job_info(driver, job)
    print('|----------|')
    print(current_job,total_jobs)
    current_job += 1
    print(title, company, location)
    print(description)
    time.sleep(1)
    
# driver.get method() will navigate to a page given by the URL address
for i in range(25,total_jobs,25):
    search_url = 'https://www.linkedin.com/jobs/search/?f_E=2&f_TPR=r604800&f_WRA=true&geoId=103644278&keywords=(data%20scientist)AND(python)AND(git)&location=United%20States&sortBy=DD'
    driver.get(search_url + '&start=' + str(i))
    time.sleep(5)
    
    jobs = set_up_job_search(driver)

    for i, job in enumerate(jobs):
        print()
        job.click()
        time.sleep(1.5)
        title, company, location, description = get_job_info(driver, job)
        print(current_job,total_jobs)
        current_job += 1
        print(title, company, location)
        print(description)
        time.sleep(1)