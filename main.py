#!/usr/bin/env python
# -*- coding: utf-8 -*-
import concurrent
from concurrent.futures import ThreadPoolExecutor
import scraper

urls = list()
with open("urls.cfg", "r") as f:
    for line in f.readlines():
        urls.append(line.replace('\n', ''))


statutes = dict()

# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ProcessPoolExecutor() as executor:
    a = executor.map(scraper.download_url, urls)

scraper.write_recent_statuses()