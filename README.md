## Introduction
This is a Flask app that scrapes quizlet and brainscape websites to extract questions and answers data. The scraped data is returned as a JSON response. The supported platforms are the following:
```
https://quizlet.com/
https://www.brainscape.com/flashcards
https://www.cram.com/flashcards
```

## Requirements
To run the code, you will need:

```
Python 3.x
Flask
Selenium
Chromedriver
```
## How to Use
Install the required packages by running pip install -r requirements.txt
Start the Flask app by running python api_main.py
You can access the scraped data by sending a GET request to the following endpoints:
```
/api/data/quizlet/<string:url>
```
```
/api/data/brainscape/<string:url>
```
Note: The URL should be base64 encoded to prevent issues with special characters in the URL.
Note: The request can take up too 20 seconds

## Code Explanation
The code uses the Selenium library to control a Chrome webdriver and extract data from the website. It uses the Chrome webdriver to load the URL and interacts with the web elements on the page. The scraped data is stored in a dictionary and returned as a JSON response through the Flask app.
