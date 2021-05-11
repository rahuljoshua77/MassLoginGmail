from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
import random
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from multiprocessing import Pool
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import re

cwd = os.getcwd()

opts = Options()
opts.headless = True
opts.add_argument('log-level=3') 
dc = DesiredCapabilities.CHROME
dc['loggingPrefs'] = {'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}
opts.add_argument('--ignore-ssl-errors=yes')
opts.add_argument("--start-maximized")
opts.add_argument('--ignore-certificate-errors')
opts.add_argument('--disable-blink-features=AutomationControlled')
opts.add_experimental_option('excludeSwitches', ['enable-logging'])
path_browser = f"{cwd}\chromedriver.exe"

def login_email():
    
    global element
    global browser
    global email
    global password

    try:        
        element = wait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#identifierId")))
        element.send_keys(email)
            
        sleep(0.5)
        element.send_keys(Keys.ENTER) 
        sleep(2)   
        element = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
        
        element.send_keys(password)
        sleep(0.5)
        element.send_keys(Keys.ENTER)  
  
        sleep(5)
       
        if "/signin/v2/challenge/" in browser.current_url:
            try:
                element = wait(browser,5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="headingText"]/span'))).text

                with open('failedLogin.txt','a') as f:
                    f.write('{0}|{1}\n'.format(email,password))

                print(f"[*] [ {email} ] Failed Login Gmail: [ {element} ]")
                browser.quit()
            except:
        
                with open('failedUnknown.txt','a') as f:
                    f.write('{0}|{1}\n'.format(email,password))
                print(f"[*] [ {email} ] Login Login [ Password Incorrect/Unknown Error ]")
                browser.quit()
        else:
            try: 
                wait(browser,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#accept"))).click()
            except:
                pass 

            with open('succesLogin.txt','a') as f:
                f.write('{0}|{1}\n'.format(email,password))
            print(f"[*] [ {email} ] Success Login")
            browser.quit()
            
    except Exception as e:
    
        sleep(2)
        print(e)  
        with open('failedLogin.txt','a') as f:
            f.write('{0}|{1}\n'.format(email,password))
         
        print(f"[*] [ {email} ] Failed Login Gmail")

def open_browser(k):
    
    global browser
    global element
    global email
    global password
    k = k.split("|")
    email = k[0]
    password = k[1]
    random_angka = random.randint(100,999)
    random_angka_dua = random.randint(10,99)
    opts.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.{random_angka}.{random_angka_dua} Safari/537.36")
    browser = webdriver.Chrome(options=opts, desired_capabilities=dc, executable_path=path_browser)
    browser.get("https://accounts.google.com/signin/v2/identifier?hl=id&refresh=1)%2C&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
    login_email()
     
if __name__ == '__main__':
    global list_accountsplit
    global k
    print("[*] Automation Login Gmail")
    print("[*] Author: RJD")
    jumlah = int(input("[*] Multi Processing: "))
    print("[*] Proccess...")
    
    file_list = "gmail.txt"
    myfile = open(f"{cwd}/{file_list}","r")
    list_account = myfile.read()
    list_accountsplit = list_account.split()
    k = list_accountsplit
    with Pool(jumlah) as p:  
        p.map(open_browser, k)
            
    print("[*] ===================================")
    print("[*] Automation Complete!!")
            
     
