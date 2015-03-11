# Functional tests for TDD tutorial

from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

# page should have 'Django' in the title
assert 'Django' in browser.title
