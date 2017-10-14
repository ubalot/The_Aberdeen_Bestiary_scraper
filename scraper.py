#!/usr/bin/python2

import os
import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from pyvirtualdisplay import Display


HOME_FOLDER = os.environ['HOME']
DOWNLOAD_FOLDER = os.path.join(HOME_FOLDER, 'Downloads', 'ms24')

# HIDE BROWSER
# display = Display(visible=0, size=(800, 600))
# display.start()

fp = webdriver.FirefoxProfile()

fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", DOWNLOAD_FOLDER)
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "jpg")


# START FIREFOX INSTANCE
browser = webdriver.Firefox(firefox_profile=fp)

# TIME TO WAIT JAVASCRIPT TO LOAD
wait = WebDriverWait(browser, 60)

# SCRAPE URL
manuscript_url = 'https://www.abdn.ac.uk/bestiary/ms24'

# OPEN SCRAPE URL
browser.get(manuscript_url)


def wait_for_element(css_selector):
    """
    Wait until element shows on page (WebDriverWait declare time before TimeOutException is raised)
    """
    try:
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
    except selenium.common.exceptions.TimeoutException:
        print('Timeout exception for selector:', css_selector)


def query_elements(css_selector):
    """ Return an elements, wait for them if they are not on page. """
    elements = []
    try:
        wait_for_element(css_selector)
        elements = browser.find_elements_by_css_selector(css_selector)
    except (selenium.common.exceptions.NoSuchElementException,
            selenium.common.exceptions.TimeoutException):
        elements = None
    return elements


def query_element(css_selector):
    """ Return an element, wait for it if it's not on page. """
    element = None
    try:
        wait_for_element(css_selector)
        element = browser.find_element_by_css_selector(css_selector)
    except (selenium.common.exceptions.NoSuchElementException,
            selenium.common.exceptions.TimeoutException):
        element = None
    return element


# first page (1r) need a different selector.
first_page = "body > div.row.small-up-1.medium-up-2.large-up-4 > div:nth-child(1) > div > div > div:nth-child(2) > a"
link_selector = ".column > .row.collapse > .small-6.columns > a"
elements = [query_element(first_page)] + query_elements(link_selector)
page_links = [e.get_attribute('href') for e in elements]

for page_link in page_links:
    # print(page_link)
    browser.get(page_link)
    image_selector = "#download > img"
    download_image = query_element(image_selector)
    download_image.click()
    time.sleep(3)


browser.close()
