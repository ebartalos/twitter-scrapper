#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


def notify(title, text):
    os.system("""
              osascript -e 'display notification "%s" with title "%s"'
              """ % (text, title))


def text_to_push(tw_dict):
    text = ''
    for key, value in tw_dict.items():
        if value != '':
            text = text + '\n' + value.replace("\'", "")

    return text


urls = list()
with open("urls.cfg", "r") as f:
    for line in f.readlines():
        urls.append(line.replace('\n', ''))


chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=chrome_options)

while True:
    for url in urls:
        print("Scraping " + url)
        tw = dict()
        tw.items()
        driver.get("https://twitter.com/" + url)
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        tw_timestamp = driver.find_element_by_xpath(
            "//div[contains(@class, 'original-tweet')]//small[@class = 'time']//a//span[contains(@class, 'timestamp')]").text

        tw['timestamp'] = tw_timestamp + ' ago'
        if 's' not in tw_timestamp and 'now' not in tw_timestamp:
            continue

        else:
            if 's' in tw_timestamp:
                tw_timestamp = tw_timestamp.rstrip('s')
                if int(tw_timestamp) > 35:
                    print("Too long timeout for " + url)
                    continue

            # rtw
            if 'Retweeted' in driver.find_element_by_xpath("((//div[contains(@class, 'original-tweet')])[1])").text:
                tw['retweet'] = 'Retweeted'
            else:
                tw['retweet'] = ''

            tw_text = driver.find_element_by_xpath(
                "(//div[contains(@class, 'original-tweet')]//div[@class = 'js-tweet-text-container']//p[contains(@class, 'tweet-text')])[1]").text
            tw_text.replace('\n', '')
            tw['text'] = 'Text present'

            try:
                tw_img = driver.find_element_by_xpath(
                    "((//div[contains(@class, 'original-tweet')])[1])//div[@class = 'AdaptiveMedia-singlePhoto']//img").get_attribute(
                    "src")
                tw['img'] = 'Image present'
            except NoSuchElementException:
                tw['img'] = ''

            try:
                tw_vod = driver.find_element_by_xpath(
                    "((//div[contains(@class, 'original-tweet')])[1])//div[@class = 'AdaptiveMedia-video']")
                tw['video'] = 'Video present'

            except NoSuchElementException:
                tw['video'] = ''

            print(text_to_push(tw))
            notify(url, text_to_push(tw))
    time.sleep(10)
