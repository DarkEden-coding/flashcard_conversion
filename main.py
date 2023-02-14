from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep
from flask import Flask, jsonify
import base64

app = Flask(__name__)


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-setuid-sandbox")

    driver = webdriver.Chrome()
    driver.set_window_size(1800, 1080)
    return driver


@app.route("/api/data/quizlet/<string:url>", methods=["GET"])
def get_quizlet_data(url):
    url = base64.urlsafe_b64decode(url.encode()).decode()
    print(f"Getting quizlet data from {url}")

    driver = create_driver()

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
    sleep(1)

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
    url = base64.urlsafe_b64decode(url.encode()).decode()
    print(f"Getting brainscape data from {url}")

    driver = create_driver()

    # load page
    driver.get(url)

    # wait for page to load
    WebDriverWait(driver, 30).until(
        ec.presence_of_element_located((By.CLASS_NAME, "smart-card-row"))
    )

    sleep(1)

    # get all cards
    elements = driver.find_element(
        By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div[3]/div[2]"
    ).find_elements(By.CLASS_NAME, "smart-card-row")

    # dict to store questions and answers
    questions = {}

    for element in elements:
        element = element.find_element(By.XPATH, "./section")

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


@app.route("/api/data/cram/<string:url>", methods=["GET"])
def get_cram_data(url):
    url = base64.urlsafe_b64decode(url.encode()).decode()
    print(f"Getting cram data from {url}")

    driver = create_driver()

    # load page
    driver.get(url)

    # wait for page to load
    WebDriverWait(driver, 30).until(
        ec.presence_of_element_located((By.CLASS_NAME, "card"))
    )

    sleep(1)

    number_of_cards = (
        int(
            driver.find_element(
                By.XPATH, """//*[@id="tablePagination_totalPages"]"""
            ).text
        )
        * 10
    )

    elements = []
    for i in range(number_of_cards):
        try:
            element = driver.find_element(By.XPATH, f"""//*[@id="row{i + 1}"]""")
            elements.append(element)
        except:
            break

    # dict to store questions and answers
    questions = {}

    for element in elements:
        question = element.find_element(
            By.CLASS_NAME,
            "question",
        ).text

        answer = element.find_element(
            By.CLASS_NAME,
            "answer",
        ).text

        if question != "":
            print(f"Question: {question}")
            print(f"Answer: {answer}")
            questions[question] = answer

    driver.quit()

    return jsonify(questions)


@app.route("/api/data/ping/", methods=["GET"])
def ping():
    return jsonify({"status": "success"})


if __name__ == "__main__":
    app.run(debug=True, port=15204)
