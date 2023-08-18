import json
from asyncio import sleep

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from regex import is_valid_url


# URL to the webpage you want to scrape
async def scrape(url):
    options = Options()
    options.headless = True

    # Set up the Selenium WebDriver using GeckoDriver for Firefox
    driver = webdriver.Firefox(options=options)

    # Navigate to the URL
    driver.get(url)
    await sleep(5)


    # Get the page source (HTML content)
    # click_element = driver.find_element(By.CSS_SELECTOR, 'span[title="II tur"]')
    #
    # # Click on the element
    # click_element.click()
    page_source = driver.page_source

    # Close the driver
    driver.quit()

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    b_questions = soup.find_all('div', class_='b-question')
    data = {}
    comments = {}
    meyar = {}
    # if len(b_questions) == 0:
    #     b_questions = soup.find_all('div', class_='b-theme')

    # Print the contents of the found <div> elements
    for question in b_questions:
        question_text = question.find('div', class_='b-question-content').text
        question_answer = question.find_all('div', class_='b-answer')
        for answer in question_answer:
            if "Cavab:" in answer.text:
                answer_text = answer.text
                data[question_text] = answer_text
            elif "Şərh:" in answer.text:
                comment = answer.text
                comments[question_text] = comment
            elif "Meyar:" in answer.text:
                meyar_text = answer.text
                meyar[question_text] = meyar_text

    return data, comments, meyar