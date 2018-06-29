'''
This is a scraper for linkedin, it has several dependencies that I am working on cutting down but as it stands currently, this project depends on the following:
time, selenium, tqdm, pyfiglet, pip, and that python is in your system path

Selenium and time are imported in the code, as for all the others, the easiest way to install them is through pip ie 'pip install tqdm' 
please note that even after the required dependencies have been installed via pip they must still be imported here ie: import tqdm
'''
try:
    import time
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from tqdm import tqdm
    from pyfiglet import figlet_format
    import sys 
    import multiprocessing
    import csv


except :
    print(' You are attempting to run this python script and you have unmet dependencies or incorrect import statements. \
please see the comments at the top of the file or the readme on github how to solve this problem')
    sys.exit()


def banner ():
        print(figlet_format('PY SCRAPER 1.0', font = 'smslant'))
    
def final():
    print(figlet_format('SEE YOU SPACE COWBOY . . .', font = 'smslant'))




    
def start(list):
    try:
        banner()
        populateNamesList(list)
    except FileNotFoundError :
        print('Not a valid datatype, we need a file to parse!')
    
               
                
def populateNamesList(file):
    nameslist = []    
    try:
        file = open(file,'r')
        
        f = file.readlines()
        
        for lines in f:
            nameslist.append(lines)
        file.close()

        pool = multiprocessing.Pool()
        pool.apply_async(parseNamesList(nameslist))
        
        pool.close()
        pool.join()
        final()    
    except FileNotFoundError:
        print('There was an error reading your file, please check if it is in the correct folder, and contains the right data and try again!')
        sys.exit()


def parseNamesList(nameslist):
        
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--headless") option for headless browsing, be warned it increases you chances of getting caught but greatly speed up processes
    driver = webdriver.Chrome(chrome_options = chrome_options)
    # print(nameslist[0]) this is also for debugging purposes, if the link comes up as ï»¿+ some valid URL then you need to remove what is called "Byte order mark" from the file
    driver.get(nameslist[0])
    time.sleep(3)
    driver.find_element_by_css_selector('#join-form > p.form-subtext.login > a').click()
    time.sleep(3)
    driver.find_element_by_css_selector('#login-email').send_keys("EMAIL")
    driver.find_element_by_css_selector('#login-password').send_keys("PASSWORD")
    driver.find_element_by_css_selector('#login-submit').click()
    file = open('output1.csv','w',newline = '')
    debugfile = open('debugfile.txt','w') 
    fieldnames = ['name','employment','link_comments']
    writer = csv.DictWriter(file,fieldnames=fieldnames)
    writer.writeheader()
        
    for i in tqdm(range(len(nameslist))):
        try:
                
            driver.get(nameslist[i])
            time.sleep(30)    
            content = driver.page_source
            
            
            soup = BeautifulSoup(content,'html.parser')
            name_box = soup.find('h1',attrs={'class':'pv-top-card-section__name Sans-26px-black-85%'})
            
            
            currentjob = soup.find('h3',attrs = {'class':'Sans-17px-black-85%-semibold'}) # if you use h3 and class as Sans-17px-black-85%-semibold you can find employment but only employment field nothing about the org will be preserved, div and pv-entity__summary-info give you more info but are prone to more errors 
            current_job_to_text = currentjob.text.strip()
            writer.writerow({'name': name_box.text.strip(),'employment':current_job_to_text})
            time.sleep(3)
            
            
                
        except Exception as e:
            writer.writerow({'name':'*','employment':'*','link_comments':'The bot caught that this link may be bad, please verify manually '+nameslist[i]})
            pass
            
        except KeyboardInterrupt :
            print("Keyboard interrupt detected!, Goodbye!")
            final()
            sys.exit()
    file.close()    
    driver.quit()
    

if __name__== "__main__":
    start("FILE_OF_LINKS.txt")
    
    
   

    
