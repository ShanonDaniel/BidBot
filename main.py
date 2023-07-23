import time
import json
import argparse
import os
import csv
import sys

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from restricted_input import r_input

from setting import *
from config import *
from functions import *

def getText(driver, xpath)->str:
    return fnGetElementXpath(driver, False, xpath).__getattribute__('text')

def setText(driver, xpath, val)->bool:
    #Set up text
    try:
        ele = fnGetElementXpath(driver, False, xpath)

        actions = ActionChains(driver)
        actions.click(on_element = ele)
                
        actions.key_down(Keys.CONTROL).send_keys('A').key_up(Keys.CONTROL)            
        actions.send_keys(f'{val}')
        actions.perform()
        return True
    except:
        return False

if __name__ == '__main__':
    os.system('cls')
    parser = argparse.ArgumentParser(description="Make an account in Upwork")
    parser.add_argument('-in', '--index_number', help = "Pass --index_number to the mail and the name of octo profile", type = int, default = 1, required = True)
    args = parser.parse_args()

    with open('elements.json') as fp:
        elements = json.loads(fp.read())
    
    profile_id = ''

    # Delete Profile
    try:
        profile_id = fnGetUUID(f'{OCTO_ID}')
        deleteProfile(profile_id)
        print(f'Success to delete {OCTO_ID}!')
    except:
        try:
            forcestop_profile(profile_id)
            deleteProfile(profile_id)
        except:
            print(f'There does not exist with profile name {OCTO_ID}')
    
    # Create Profile
    try:
        profile_id = fnGetUUID(f'{OCTO_ID}')
    except:
        print(f'Create Octo Profile with {OCTO_ID}')
        profile_id = createProfile(f'{OCTO_ID}')

    port = get_debug_port(profile_id)
    driver = get_webdriver(port)
    driver.get(UPWORK_LOGIN_URL)
    
    time.sleep(1)
    
    # Decline cookie saving
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#onetrust-close-btn-container button'))
        )
    except:
        pass
    
    time.sleep(1)
    try:
        ele = driver.find_element(By.CSS_SELECTOR, '#onetrust-close-btn-container button')
        ele.click()
    except:
        print('Can\'t click the close button!')
        pass
    
    # Login with your account with index number
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input#login_username'))
        )
    except:
        pass
    try:
        ele = driver.find_element(By.CSS_SELECTOR, 'input#login_username')
        actions = ActionChains(driver)
        actions.click(on_element = ele)
        actions.key_down(Keys.CONTROL).send_keys('A').key_up(Keys.CONTROL)
        actions.send_keys(f'{EMAIL}+{int(args.index_number)}@proton.me')
        actions.perform()
    except:
        print('Can\'t input username!')

    try:
        ele = driver.find_element(By.CSS_SELECTOR, 'button#login_password_continue')
        ele.click()
    except:
        print('Can\'t click the continue button!')

    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input#login_password'))
        )
    except:
        pass

    try:
        ele = driver.find_element(By.CSS_SELECTOR, 'input#login_password')
        actions = ActionChains(driver)
        actions.click(on_element = ele)
        actions.key_down(Keys.CONTROL).send_keys('A').key_up(Keys.CONTROL)
        actions.send_keys(PASSWORD)
        actions.perform()
    except:
        print('Can\'t input password!')

    try:
        ele = driver.find_element(By.CSS_SELECTOR, 'button#login_control_continue')
        ele.click()
    except:
        print('Can\'t click the continue button!')
        pass
    
    driver.set_window_size(1100, 1180)
    
    try:
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.up-modal-footer button'))
        )
    except:
        pass
    
    time.sleep(2)
    try:
        ele = driver.find_element(By.CSS_SELECTOR, 'div.up-modal-footer button')
        ele.click()
    except:
        print('Can\'t click the close button!')

    time.sleep(1)
    try:
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.up-btn.up-btn-primary[data-test="job-search-button"]'))
        )
    except:
        print('Can\'t load overview page!')

    nobid_jobs_list = []
    
    with open('joblist.csv', 'r+') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
              if row == ['']: continue
              nobid_jobs_list = row
              break
    f.close()

    time.sleep(1)
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[aria-labelledby="cfe-job-search-label"]'))
        )
    except:
        pass
    time.sleep(2)
    try:
        ele = driver.find_element(By.CSS_SELECTOR, 'input[aria-labelledby="cfe-job-search-label"]')
        actions = ActionChains(driver)
        actions.click(on_element=ele)
        actions.send_keys(JOBSEARCHITEMS)
        actions.perform()
    except:
        print('Can\'t type the search items!')
    
    time.sleep(3)
    try:
        ele = driver.find_element(By.CSS_SELECTOR, 'button.up-btn.up-btn-primary[data-test="job-search-button"]')
        ele.click()
    except:
        print('Can\'t click the Job Search button')
    
    time.sleep(1)    
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'section.up-card-list-section'))
        )
    except:
        print('Can\'t load jobs page!')
    
    time.sleep(2)
    try:
        js_script = 'document.querySelector("input[type = \\"checkbox\\"][data-test = \\"filter-hourly-job-type\\"]").click();'
        driver.execute_script(js_script)
    except:
        print('Can\'t click hourly job type checkbox!')
    
    time.sleep(2)
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'section.up-card-list-section'))
        )
    except:
        print('Can\'t load jobs page!')

    job_links = []    
    try:
        js_script = 'eles = document.querySelectorAll("section.up-card-list-section");\
            var i = 0;\
            job_links = [];\
            for (i = 0; i < eles.length; i++) {\
                if (eles[i].querySelector("strong[data-test=\\"job-type\\"]").textContent.indexOf("Hourly") != -1)\
                    job_links.push(eles[i].querySelector("a.up-n-link[data-test = \\"UpLink\\"]").getAttribute("href"));\
            }\
            return job_links;'
        job_links = driver.execute_script(js_script)
    except:
        print("Thre is no hourly jobs!")
    job_links.reverse()

    for job_link in job_links:
        job_id = job_link.split('/')[-2].split('_')[-1]
        flg = False
        for i in range(len(nobid_jobs_list)):
            if nobid_jobs_list[i] == job_id:
                flg = True
                break
        if flg:
            continue
        nobid_jobs_list.append(job_id)

    while True:
        if len(nobid_jobs_list) > 0:
            break
        time.sleep(30)
        driver.refresh()
        job_links = []    
        try:
            js_script = 'eles = document.querySelectorAll("section.up-card-list-section");\
                var i = 0;\
                job_links = [];\
                for (i = 0; i < eles.length; i++) {\
                    if (eles[i].querySelector("strong[data-test=\\"job-type\\"]").textContent.indexOf("Hourly") != -1)\
                        job_links.push(eles[i].querySelector("a.up-n-link[data-test = \\"UpLink\\"]").getAttribute("href"));\
                }\
                return job_links;'
            job_links = driver.execute_script(js_script)
        except:
            print("Thre is no hourly jobs!")
        job_links.reverse()
        
        for job_link in job_links:
            job_id = job_link.split('/')[-2].split('_')[-1]
            flg = False
            for i in range(len(nobid_jobs_list)):
                if nobid_jobs_list[i] == job_id:
                    flg = True
                    break
            if flg:
                continue
            nobid_jobs_list.append(job_id)

    job_id = nobid_jobs_list.pop(0)
    # print(nobid_jobs_list)
    # Update CSV file:
    with open ('joblist.csv', 'w+', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(nobid_jobs_list)
    f.close()

    driver.get(f'https://www.upwork.com/ab/proposals/job/{job_id}/apply/')
    
    modalFlg = True
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.up-modal-footer button'))
        )
    except:
        modalFlg = False
        print('There is no modal to help beginners!')
        pass
    
    time.sleep(1)
    if modalFlg:
        while True:
            try:
                ele = driver.find_element(By.CSS_SELECTOR, "div.up-modal-footer button")
                ele.click()
                break
            except:
                print('Can\'t click the close button!')
    
    time.sleep(1)
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'textarea[aria-labelledby="cover_letter_label"]'))
        )
    except:
        print('There is no coverletter text area!')
        pass
    
    try:
        js_script = 'eles = document.querySelectorAll("button.up-btn-default");\
            var i = 0;\
            for (i = 0; i < eles.length; i++) {\
                if (eles[i].textContent.indexOf("Set a bid") != -1)\
                    break;\
            }\
            eles[i].click();'
        driver.execute_script(js_script)
    except:
        print("Can\'t click the set a bid button!")

    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[aria-describedby="bid-connects-label"]'))
        )
    except:
        print('There is no input to type connect numbers!')
        pass
    
    time.sleep(1)
    try:
        ele = driver.find_element(By.CSS_SELECTOR, 'input[aria-describedby="bid-connects-label"]')
        actions = ActionChains(driver)
        actions.click(on_element = ele)
        actions.key_down(Keys.CONTROL).send_keys('A').key_up(Keys.CONTROL)
        actions.send_keys('22')
        actions.perform()
    except:
        print('Can\'t write connect numbers!')

    try:
        js_script = 'eles = document.querySelectorAll("button.up-btn-default");\
            var i = 0;\
            for (i = 0; i < eles.length; i++) {\
                if (eles[i].textContent.indexOf("Bid") != -1)\
                    break;\
            }\
            eles[i].click();'
        driver.execute_script(js_script)
    except:
        print("Can\'t click Bid button!")
        pass

    time.sleep(3)

    try:
        ele = driver.find_element(By.CSS_SELECTOR, 'textarea[aria-labelledby="cover_letter_label"]')
        actions = ActionChains(driver)
        actions.click(on_element = ele)
        actions.send_keys(BID_PHRASE)
        actions.perform()
    except:
        print('Can\'t write bid phrase!')
        
    time.sleep(1)
    
    try:
        js_script = 'eles = document.querySelectorAll("button.up-btn-primary");\
            var i = 0;\
            for (i = 0; i < eles.length; i++) {\
                if (eles[i].textContent.indexOf("Send") != -1)\
                    break;\
            }\
            eles[i].click();'
        driver.execute_script(js_script)
    except:
        sys.exit("Can\'t click Send button!")
        pass
    time.sleep(1)
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type = "checkbox"]'))
        )
    except:
        stop_profile(profile_id)
        time.sleep(3)
        sys.exit("We can't bid! Please fix errors and manually bid!")
        
    try:
        ele = driver.find_element(By.CSS_SELECTOR, 'input[type = "checkbox"]')
        ele.click()
    except:
        print('Can\'t click the checkbox!')
    
    time.sleep(1)
    try:
        js_script = 'eles = document.querySelectorAll("button.up-btn-primary");\
            var i = 0;\
            for (i = 0; i < eles.length; i++) {\
                if (eles[i].textContent.indexOf("Submit") != -1)\
                    break;\
            }\
            eles[i].click();'
        driver.execute_script(js_script)
    except:
        print("Can\'t click Submit button!")
        pass
    
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[aria-labelledby="snackbar-default-content"]'))
        )
    except:
        pass


    driver.save_screenshot(f"./image/{job_id}.png")
    stop_profile(profile_id)

    time.sleep(3)
                