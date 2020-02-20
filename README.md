# amazon-top-deals-python

A program to find the top 5 best deals fro any given product on amazon

## About

This program will open top 5 best deals for a given product in your default browser.
Best deals are decided based on the current selling price and the actual price (i.e. the crossed out one)
My goal while creating this was to lower the manual labour of browsing all the search result pages.
While this might not be 100% accurate (as the prices may not be 100% accurate) it certainly will help out some of us.

NOTE: Right now this shows only products with 4 stars and up which can be tweaked according to your need. But in future releases I might add a feature to set the option for required rating and other stuff etc.

Hope you like this pet project

## Requirements

* Python 3.7^
* Selenium-Webdriver
* Chromedriver for selenium

## How to use

* First make sure that chromedriver.exe is downloaded and copied to a folder named driver in the same folder where the Crawler.py is stored (or store it anywhere but make changes to the path inside the code)
* If running for first time then first run setup.bat

* To run the program double click on run.py or open terminal/commandprompt in same folder and type `python run.py` and press enter

### This project is licensed under the [MIT license](https://raw.githubusercontent.com/Shetty073/amazon-top-deals-python/master/LICENSE)
