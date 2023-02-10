from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep
from flask import Flask, jsonify
import base64

app = Flask(__name__)


@app.route("/api/data/quizlet/<string:url>", methods=["GET"])
def get_quizlet_data(url):
    # load chrome driver
    options = Options()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/84.0.4147.125"
        "Safari/537.36 "
    )
    # options.add_argument("--headless")
    options.add_argument("--silent")
    options.add_argument("log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1800, 1080)

    url = base64.urlsafe_b64decode(url.encode()).decode()

    # load page
    driver.get(url)

    while True:
        try:
            # wait for page to load
            driver.find_element(By.CLASS_NAME, "SetPageTerms-term")
            break
        except:
            try:
                close = driver.find_element(
                    By.CLASS_NAME, """//*[@id="bx-close-inside-1214140"]"""
                )
                close.click()
                break
            except:
                sleep(0.2)
                pass

    # wait for page to load
    WebDriverWait(driver, 30).until(
        ec.presence_of_element_located((By.CLASS_NAME, "SetPageTerms-term"))
    )

    driver.execute_script("window.scrollTo(0, 500)")
    sleep(2)

    # dict to store questions and answers
    questions = {}

    # get all cards
    non_hidden_elements = driver.find_elements(By.CLASS_NAME, "SetPageTerms-term")

    for element in non_hidden_elements:
        try:
            question, answer = element.text.replace(".", "").split("\n")
        except ValueError:
            question = element.text.replace(".", "")
            answer = ""

        if question != "":
            print(f"Question: {question}")
            print(f"Answer: {answer}")
            questions[question] = answer

    hidden_elements = driver.find_elements(
        By.CLASS_NAME, "SetPageTerms-term SetPageTerms-term--beyondSignupThreshold"
    )

    for element in hidden_elements:
        text = element.find_elements(By.CLASS_NAME, "TermText notranslate lang-en")

        question = text[0].text.replace(".", "")
        answer = text[1].text.replace(".", "")

        if question != "":
            print(f"Question: {question}")
            print(f"Answer: {answer}")
            questions[question] = answer

    driver.quit()

    return jsonify(questions)


@app.route("/api/data/brainscape/<string:url>", methods=["GET"])
def get_brainscape_data(url):
    # load chrome driver
    options = Options()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/84.0.4147.125"
        "Safari/537.36 "
    )
    options.add_argument("--headless")
    options.add_argument("--silent")
    options.add_argument("log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1800, 1080)

    url = base64.urlsafe_b64decode(url.encode()).decode()

    # load page
    driver.get(url)

    # wait for page to load
    WebDriverWait(driver, 30).until(
        ec.presence_of_element_located((By.CLASS_NAME, "smart-card-row"))
    )

    sleep(2)

    # get all cards
    elements = driver.find_element(
        By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div[3]/div[2]"
    ).find_elements(By.CLASS_NAME, "smart-card-row")

    print(f"Number of cards: {len(elements)}")

    # dict to store questions and answers
    questions = {}

    for element in elements:
        element = element.find_element(By.XPATH, "./section")

        # print element class name
        print(element.get_attribute("class"))

        question = element.find_element(
            By.XPATH,
            "./div[1]",
        ).text.replace("Q\n", "")

        answer = element.find_element(
            By.XPATH,
            "./div[2]",
        ).text.replace("A\n", "")

        if question != "":
            print(f"Question: {question}")
            print(f"Answer: {answer}")
            questions[question] = answer

    driver.quit()

    return jsonify(questions)


if __name__ == "__main__":
    app.run(debug=True)
