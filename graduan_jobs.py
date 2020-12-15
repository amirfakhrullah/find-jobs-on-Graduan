from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from bs4 import BeautifulSoup
import time
import pprint
from job_description import job_description


search = str(input('What kind of position are you looking for?\n:'))
search = search.split()
driver = webdriver.Chrome()
url = 'https://graduan.com/jobs?page=1'
driver.get(url)


# to loop between pages
page = 1
loop = True
while loop:
    driver.implicitly_wait(3)   
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '#career-list > section:nth-child(2) > div > div.col-md-8.pr-40 > div')))
    except:
        break

    html = driver.page_source
    soup = BeautifulSoup(html, 'html5lib')
    jobs = soup.find_all('div', {'class':'item'})

    if len(jobs) == 0: break
    # to loop between jobs shown in the page
    for job in jobs:
        role = job.find('h4', {'class':'margin-bottom-5'}).text
        check = True
        for word in search:
            # to make sure the job search matches the title of the job
            if word.lower() not in role.lower():
                check = False
                break
        if check == True:
            # store the jobs in a dictionary from job_description.py
            job_desc = job_description(role)
            try:
                # store the name of the comnpany
                company = job.find('p').text
                job_desc['2. Company'] = company
            except:
                Exception()
            #store the date posted
            posted = job.find('span', {'class':'moment-humanize'}).text
            job_desc['3. Posted'] = posted
                
            # store the href link to apply for the job
            apply = job.find('a', href=True)
            job_desc['4. To apply'] = apply['href']
            pprint.pprint(job_desc)
    
    # to move to the next page
    page += 1
    try:
        driver.get(driver.current_url[:-1] +  str(page))
    except:
        loop = False
        break

