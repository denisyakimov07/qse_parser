import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from sqlalchemy.orm import sessionmaker
from selenium.webdriver.common.by import By
from selenium import webdriver
import os
from selenium.webdriver.support.wait import WebDriverWait

from bs4 import BeautifulSoup
from sqlalchemy import create_engine

from environment import get_env
from models_qse_news import QSENews

DATABSE_URI = f'{get_env().DB_DATABASE_TYPE}://{get_env().DB_USER}' \
              f':{get_env().DB_PASSWORD}@{get_env().DB_HOST}' \
              f':{get_env().DB_PORT}/{get_env().DB_DATABASE}'

engine = create_engine(DATABSE_URI, echo=False)
Session = sessionmaker(bind=engine)
session = Session()


def creat_chrome():
    chrome_options = Options()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
    return driver


# def creat_chrome():
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--no-sandbox")
#     driver = webdriver.Chrome()
#     return driver


def save_news(url, company_tag):
    if not session.query(QSENews).filter(QSENews.news_url == url).first():
        print(url)
        text_body = ''
        driver = creat_chrome()
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.ID, "DisplayNewsDetails_main_div")))
        innerHTML = driver.execute_script("return document.documentElement.outerHTML")

        soup = BeautifulSoup(innerHTML, 'lxml')
        news_title = str(soup.find('h1', class_="pink-color large-title").text).replace(" ", '').strip()
        news_data = soup.find('p', id="publishdate").text
        datetime_news = datetime.datetime.strptime(f"{news_data}T10:10:10-0005", '%d %b %YT%H:%M:%S%z')

        news_download_attachment_url = soup.find_all("a", href=True)
        download_attachment_url = None
        for i in news_download_attachment_url:
            if "https://www.qe.com.qa/qdisclosure" in i['href']:
                download_attachment_url = i['href']

        news_body = soup.find(class_="p-18")
        for i in news_body.next_siblings:
            text_body = text_body + (
                str(i.text).replace("Click here to download attachment", '').replace("n\\", '').strip().replace(" ",
                                                                                                                ''))

        add_news = QSENews()
        add_news.company_title = company_tag
        add_news.news_date = datetime_news
        add_news.news_download_attachment_url = download_attachment_url
        add_news.news_url = url
        add_news.news_title = news_title
        add_news.news_body = text_body
        session.add(add_news)
        session.commit()
        return


def get_company_tags():
    company_list_url = "https://qe.com.qa/en/web/guest/listed-companies"
    driver = creat_chrome()
    driver.get(company_list_url)
    WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.ID, "div1")))
    innerHTML = driver.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(innerHTML, 'lxml')
    tags = soup.find_all("p", class_="companyCode")
    tags_list = []
    for i in tags:
        tags_list.append(i.text)

    return tags_list


def get_company_news_list(url):
    news_url_list = []
    driver = creat_chrome()
    driver.get(url)
    WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.ID, "news-content")))
    innerHTML = driver.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(innerHTML, 'lxml')
    test = soup.find_all("div", class_="col-lg-6 col-md-12 p-2")
    for i in test:
        news_url_list.append(f'https://qe.com.qa/en/{i.find("a", href=True)["href"]}')

    return news_url_list


print("start scraping")

op = webdriver.ChromeOptions()
op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
op.add_argument("--headless")
op.add_argument("--no-sandbox")
op.add_argument("--disable-dev-sh-usage")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=op)
print(driver.page_source)


for tag in get_company_tags():
    for news_url in get_company_news_list(f"https://qe.com.qa/en/companymoreinformationsearch?CompanyCode={tag}"):
        save_news(news_url, tag)
