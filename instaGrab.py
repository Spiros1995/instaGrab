"""
  _____           _         _____           _
 |_   _|         | |       / ____|         | |    
   | |  _ __  ___| |_ __ _| |  __ _ __ __ _| |__  
   | | | '_ \/ __| __/ _` | | |_ | '__/ _` | '_ \ 
  _| |_| | | \__ \ || (_| | |__| | | | (_| | |_) |
 |_____|_| |_|___/\__\__,_|\_____|_|  \__,_|_.__/


A simple Instagram image grabber.

How to use:
run chromedriver.exe
pip install -U selenium

instaGrab.py [email] [password] [target username] [approximate number of photos you wanna grab]
[email] = your email
[password] = your password
[target username] = the username of the profile you want to grab photos from
[approximate number of photos you wanna grab] = how many photos you wanna grab approximately

Created by Spyridon Kaloudis

"""

import time
import urllib
import sys
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import math

if len(sys.argv) < 5:
    sys.exit("You have to use the correct syntax! "
             "instaGrab.py [email] [password] [target username] [approximate number of photos you wanna grab]")

targetPersonUsername = sys.argv[3]
targetPhotosQuantity = sys.argv[4]
url = "https://www.instagram.com/" + targetPersonUsername + "/"
page = urlopen(url)
driver = webdriver.Chrome()
driver.get("https://www.instagram.com/accounts/login/?hl=en")
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='username']"))).send_keys(sys.argv[1])
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='password']"))).send_keys(sys.argv[2])

## Get rid of cookies messages
driver.find_element("xpath", '/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]').click()
time.sleep(1);

## Click the Log in button
driver.find_element("xpath", '//button[@type="submit"]').click()

## Wait for new page to load
time.sleep(5)
driver.maximize_window()
driver.get(url)
## List of image sources
imagesSrc = []
imageID = 0
## Wait for images to load on each scroll
SCROLL_PAUSE_TIME = 2
## Dictionary of images to avoid duplicates
imagesDictionary = {}
photosPerLoop = 11
loopNumber = math.ceil(int(targetPhotosQuantity)/photosPerLoop)

for i in range(0, loopNumber):
    # Scroll down to bottom to load more photos
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    # Grab any images
    imgResults = driver.find_elements(By.XPATH, "//img[contains(@src,'fna.fbcdn.net')]")
    # Add images to dictionary to avoid duplicates
    for img in imgResults:
        imagesDictionary[img.get_attribute('src')] = imageID
        imageID += 1

## Create images in folder
imageNumber = 0
for key in imagesDictionary:
    urllib.request.urlretrieve(str(key), str(imageNumber) + ".jpg".format(imageNumber))
    imageNumber += 1
