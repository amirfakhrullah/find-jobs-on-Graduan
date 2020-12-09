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

    for job in jobs:
        role = job.find('h4', {'class':'margin-bottom-5'}).text
        check = True
        for word in search:
            if word.lower() not in role.lower():
                check = False
                break
        if check == True:
            job_desc = job_description(role)
            try:
                company = job.find('p').text
                job_desc['2. Company'] = company
            except:
                Exception()

            posted = job.find('span', {'class':'moment-humanize'}).text
            job_desc['3. Posted'] = posted
                

            apply = job.find('a', href=True)
            job_desc['4. To apply'] = apply['href']
            pprint.pprint(job_desc)
            
    page += 1
    try:
        driver.get(driver.current_url[:-1] +  str(page))
    except:
        loop = False
        break

