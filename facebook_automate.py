from selenium.webdriver.remote.remote_connection import LOGGER
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import json
import time
import re
import random

config = {}

def read_config():
    global config
    f = open('config.json')
    config = json.load(f)
    

def get_browser_instance():
    chrome_options = Options()

    chrome_driver_path = config['driver_path']
    try:
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        chrome_options.add_experimental_option("prefs",prefs)

        driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
        return driver
        

    except Exception as e:
        print(f'    [!] Chromedriver not Found on location {chrome_driver_path}. Terminationg program.')
        return None

def login(driver):
    

    email = config['fb_email']
    password = config['fb_password']
    driver.get('https://fb.com/')
    
    driver.find_element_by_id('email').send_keys(email)  #set email in text box
    driver.find_element_by_id('pass').send_keys(password) # set password in text box

    driver.find_element_by_name('login').click()  # click login button 

    return driver

def edit_profile(driver):
    print('Editing profile')
    
    profile_url = 'https://fb.com/me/'  
    time.sleep(2)

    driver.get(profile_url) # move to your profile
    time.sleep(5)
    
    driver.find_element_by_xpath('//*[@id="mount_0_0"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/span/span/div/span/div').click() # click edit 

    time.sleep(2)

    bio_text = driver.find_element_by_xpath('//*[@id="mount_0_0"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div/span/div/div/label/textarea')

    bio_text.click()
    time.sleep(2)
    bio_text.send_keys(Keys.CONTROL + 'a') # remove already available text
    bio_text.send_keys(Keys.BACKSPACE)

    updated_profile = config['updated_profile'] 

    bio_text.send_keys(updated_profile)  # set newly updated profile

    driver.find_element_by_xpath('//*[@aria-label="Save"]').click() # click save
 
    print('Edited Profile Successfully')


    return driver

def get_recent_post(source):
    post_id = re.findall('post_fbid.*?}', source) # gets all recent posts
    if post_id:
        return post_id[0].split(':')[-1][:-1] # gets the most recent post (1)
    else:
        return '0'

def comment_recent_post(driver):
    target_user = random.choice(config['profiles_to_comment'])
    
    driver.get(target_user)
    time.sleep(2)
    
        
    post_id = get_recent_post(driver.page_source)
    if post_id == '0':
        print('No posts found !')
        return driver
    
    driver.get(target_user.replace('facebook', 'm.facebook') + f'posts/{post_id}') # move to the recent post

    comment_box = driver.find_element_by_id('composerInput')
    comment_box.click()
    comment_box.send_keys(random.choice(config['comments'])) # select a random comment from config
    
    time.sleep(2)
    driver.find_element_by_name('submit').click() # post the comment 
    
    print('Comment posted successfully')
    return driver

def add_friend_from_location(driver):
    
    time.sleep(3)

    location = random.choice(config['location_to_add_friend']) # select loctaion from config
    
    print(f'Adding Friend from {location}')
    driver.get(f'https://www.facebook.com/search/people?q={location}') # search for people based on location
    time.sleep(2)

    driver.find_element_by_xpath('//*[@class="nc684nl6"]/a').click()  # select the first person
    time.sleep(10)

    driver.find_element_by_xpath('//*[@id="mount_0_0"]/div/div[1]/div/div[3]/div/div/div[2]/div[1]/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div').click() # click add friend

    print('Request sent successfully')
    return driver

if __name__ == '__main__':
    read_config()
    
    driver = get_browser_instance() # initialize selenium
    driver = login(driver) # login to facebook
    print('Logged in successfully\n')

    print('1. Edit Profile\n2. Comment Post\n3. Add friend from location\n4. Exit\n')

    # choose what to do
    while True:
        choice = int(input("Enter your choice "))
        if(choice == 1):
            driver = edit_profile(driver)

        elif(choice == 2):
            driver = comment_recent_post(driver)

        elif(choice == 3):
            driver = add_friend_from_location(driver)
        else:
            driver.quit()
            break

print('Finished')
            


    

