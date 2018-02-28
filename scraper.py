#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

statutes = dict()


def download_url(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=chrome_options)

    print("Scraping " + url)
    tw = []
    driver.get("https://twitter.com/" + url)

    if not os.path.exists(url):
        os.makedirs(url)

    with open("./" + url + "/" + 'tweets.txt', 'w', encoding="utf-8") as file_tw:
        try:
            for tweet_index in range(1, 1500):
                print(url + ": Tweet number " + str(tweet_index))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                if 'Retweeted' in driver.find_element_by_xpath("((//div[contains(@class, 'original-tweet')])[" + str(
                        tweet_index) + "])").text:
                    tw_retweet = "Retweeted"
                else:
                    tw_retweet = ''

                tw_timestamp = driver.find_element_by_xpath(
                    "(//div[contains(@class, 'original-tweet')]//small[@class = 'time']//a//span[contains(@class, 'timestamp')])[" + str(
                        tweet_index) + "]").text

                tw_text = driver.find_element_by_xpath(
                    "(//div[contains(@class, 'original-tweet')]//div[@class = 'js-tweet-text-container']//p[contains(@class, 'tweet-text')])[" + str(
                        tweet_index) + "]").text
                tw_text.replace('\n', '')
                try:
                    tw_img = driver.find_element_by_xpath("((//div[contains(@class, 'original-tweet')])[" + str(
                        tweet_index) + "])//div[@class = 'AdaptiveMedia-singlePhoto']//img").get_attribute("src")
                    urllib.request.urlretrieve(tw_img, "./" + url + "/" + tw_img.rsplit("/")[-1])
                except:
                    tw_img = ''
                try:
                    tw_vod = driver.find_element_by_xpath("((//div[contains(@class, 'original-tweet')])[" + str(
                        tweet_index) + "])//div[@class = 'AdaptiveMedia-video']")
                    # tw_vod = "https://twitter.com/i/videos/" + driver.find_element_by_xpath("((//div[contains(@class, 'original-tweet')])[" + str(
                    #     tweet_index) + "])").get_attribute("data-tweet-id")
                    # urllib.request.urlretrieve(tw_vod, url + tw_vod.rsplit("/")[-1])
                    tw_vod = "Video present"

                except:
                    tw_vod = ''
                tw.append([tw_retweet, tw_timestamp, tw_text, tw_img, tw_vod])
        except NoSuchElementException:
            print("No more tweets for " + url)
            driver.close()

        for elem in tw:
            for line in elem:
                if line != '':
                    file_tw.write(line)
                    file_tw.write("\n")
            file_tw.write("\n")

    statutes[url] = tw


def write_recent_statuses():
    # only recent statuses
    with open('statuses.txt', 'w', encoding="utf-8") as file:
        for account in statutes:
            file.write(account)
            file.write("\n")
            for elem in statutes[account]:
                if 'h' in elem[1] or 'm' in elem[1] or 'now' in elem[1]:
                    for line in elem:
                        if line != '':
                            file.write(line)
                            file.write("\n")
                    file.write("\n")
