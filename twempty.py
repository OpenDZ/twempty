#!/usr/bin/env python3.5

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from time import sleep
from fake_text import text
import os
import sys

def chromedriver():
  if getattr(sys, 'frozen', False):
    return os.path.join(sys._MEIPASS, 'chromedriver')
  else:
    return os.path.join('.', 'chromedriver')


def add_css(css):
  driver.execute_script("""
  var css = document.createElement("style");
  css.type = "text/css";
  css.innerHTML = "%s";
  document.body.appendChild(css);
  """ % (css.replace('\n', '')))

def add_overlay_div():
  add_css("""
  #twempty-overlay {
    position: fixed;
    display: none;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0,0,0,0.5);
    z-index: 2;
    cursor: pointer;
  }
  #twempty-text {
    position: absolute;
    top: 50%;
    left: 50%;
    font-size: 50px;
    color: white;
    transform: translate(-50%,-50%);
    -ms-transform: translate(-50%,-50%);
  }
  """)
  driver.execute_script("""
  const div = document.createElement('div');
  const txt_div = document.createElement('div');
  div.setAttribute('id', 'twempty-overlay');
  function off() {
    document.getElementById('twempty-overlay').style.display = "none";
  }
  function on() {
    document.getElementById('twempty-overlay').style.display = "block";
  }
  div.onclick = off;
  txt_div.setAttribute('id', 'twempty-text');
  div.appendChild(txt_div);
  document.body.appendChild(div);
  """)

def show_overlay(text=""):
  driver.execute_script("""
  document.getElementById('twempty-overlay').style.display = "block";
  document.getElementById('twempty-text').innerHTML = "%s"
  """ % text)

def hide_overlay():
  driver.execute_script("""
  document.getElementById('twempty-overlay').style.display = "none";
  """)

def init_driver():
  global driver
  options = webdriver.ChromeOptions()
  options.add_argument('--start-maximized')
  #executable_path = './chromedriver'
  executable_path = chromedriver()
  driver = webdriver.Chrome(executable_path=executable_path, chrome_options=options)
  driver.get('https://mobile.twitter.com/login')
  add_overlay_div()
  show_overlay('Please login')
  WebDriverWait(driver, 3600).until_not(
      EC.presence_of_element_located((By.CLASS_NAME, "_3m9ujp4p")))
  WebDriverWait(driver, 10).until_not(
      EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='progressbar']")))

def wipe_all():
  for caret in driver.find_elements_by_css_selector("div[data-testid='caret']"):
    caret.click()
    sleep(0.2)
    driver.find_element_by_xpath("//div[@data-testid='pin']/following-sibling::div").click()
    sleep(0.2)
    driver.find_element_by_xpath("//div[@data-testid='confirmationSheetConfirm']").click()
    sleep(0.2)
  driver.refresh()
  WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='progressbar']")))
  WebDriverWait(driver, 10).until_not(
      EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='progressbar']")))
  if len(driver.find_elements_by_css_selector("div[data-testid='caret']")): wipe_all()

def tweet(msg):
  driver.get('https://mobile.twitter.com/compose/tweet')
  WebDriverWait(driver, 10).until_not(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "div[role='progressbar']")))
  driver.find_element_by_css_selector("textarea[data-testid='tweet-textarea']").send_keys(msg)
  driver.find_element_by_css_selector("div[data-testid='tweet-button']").click()

def fake_tweet():
  tweet(text())

if __name__ == '__main__':
  init_driver()
  add_overlay_div()
  show_overlay('ready to wipe?')
  WebDriverWait(driver, 3600).until_not(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#twempty-overlay")))
  wipe_all()
  add_overlay_div()
  show_overlay('everything has been wiped')
