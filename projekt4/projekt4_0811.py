import time
import json
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options

##########################################################################################

parser = argparse.ArgumentParser(description="Description")
parser.add_argument('-filename', help='name of file with data ', type=str, default='animal_data')
args = parser.parse_args()

options = Options()
options.add_argument('--disable-notifications')

service = Service('C:/Users/Iga/Documents/kursPythonaBootCamp/PythonWZastosowanichNaukowych/projekty/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://www.reddit.com/r/dogpictures/')

buttonCookie = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH,
                '//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[3]/div[1]/section/div/section/section/form[2]/button')))
buttonCookie.click()

elements = driver.find_element(By.CSS_SELECTOR,
                               'div._2SdHzo12ISmrC8H86TgSCp _3wqmjmv3tb_k-PROt7qFZe , h3._eYtD2XCVieq6emjKBH3m')
with open(f"{args.filename}.json", "w", encoding="utf-8") as file:
    json.dump(elements.text, file, ensure_ascii=False, indent=4)
with open(f"{args.filename}.json", "r", encoding="utf-8") as data:
    print(json.dumps(json.load(data), ensure_ascii=False, indent=4))

time.sleep(5)
buttonComment = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH,
                '//*[@id="t3_qrzflt"]/div[3]/div[3]/div/div[2]/div/div/div/div[1]/a[2]')))
buttonComment.click()
time.sleep(5)

for i in range(3):
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(3)

time.sleep(10)
driver.close()
print("Web closed ...")
