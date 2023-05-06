import codecs
import concurrent.futures
import re
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as COptions
from selenium.webdriver.chrome.service import Service as CService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

session = requests.Session()
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

url = "https://www.nulled.to"
id = "atlasd"
psw = "@@Tata123"


def file_save(text: str):
    with codecs.open("a.html", mode="w", encoding="utf-8") as f:
        f.write(text)
        f.close()


resp = session.post(
    "https://www.nulled.to/index.php?app=core&module=global&section=login&do=process",
    data={
        "auth_key": "880ea6a14ea49e853634fbdc5015a024",
        "referer": "https://www.nulled.to/",
        "ips_username": id,
        "ips_password": psw,
        "anonymous": "true",
        "g-recaptcha-response": "03AL8dmw_0advVXOkJmcuPXf4cXS-23EhiBV4Izy9rAwpUufncsXewb_oIDS2eNCmo01BJRgVLeGozCF9k__MDOtJnJqfxJgTW2qLMQj_WnvxDCKmh-YuqlX5speZQXBU0OnDgY6NmB8oC_TnJEYUDFy88felAo5QWvqODtT24m0JS-GWVeh2H_8Nxdb1ofw2M9kaZCp3YG5SEIUvHIB8phJtsRnjyxGmOTfK_79peujo4AT-xcmhklhNbr9486oHiRB_EWL-t59B-aHYjD6LPxTxQ-Fuq-RlUxdzv_tiGG_sF118x8xnRNk3n2VVfU0xTBSOodsuCTyiPeV-GGrSGwl8dlvAekIC6opUy_GLDc3rRScwqPE8VCzaHfrWVj7pSFOvLgTyLoTYHhSfYRF0GHx-2fBtlnRxY1HZ5ovWdRF-6vi2UU5skspOAyUeTykwBgFfWWl1yM7aYFEVekO4ccJT-KrYszteIa8xPZaguUmkZRobzr0QZOH4h21E-441UKSv2dFDLLGt0L-i-r4H_wKl9OOfGjuqkHtEwB2y3s6lLME57638pzat6oxmFydadQ1hJndzey7AZ",
    },
    headers=headers,
)

# resp = session.get("https://www.nulled.to/index.php?app=core&module=search&do=search&andor_type=and&sid=2b04633bea30ef56751e378cee55767c&search_app_filters[forums][sortKey]=date&search_content=both&search_app_filters[forums][noPreview]=1&search_app_filters[forums][pCount]=&search_app_filters[forums][pViews]=&search_app_filters[forums][sortKey]=date&search_app_filters[forums][searchInKey]=&search_term=all&search_app=forums")

# file_save(resp.text)
# resp = session.get(url)
cookie_list = [
    {"name": x.name, "value": x.value, "domain": x.domain} for x in resp.cookies
]


options = COptions()

options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-infobars")
options.add_argument("--disable-notifications")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-save-password-bubble")
options.add_argument("--disable-translate")
options.add_argument("--enable-automation")
# options.add_argument("--headless")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--no-sandbox")
options.add_argument("--start-maximized")
options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
)
options.add_extension("./extension/buster.crx")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(
    service=CService(ChromeDriverManager().install()), options=options
)

driver.get(url)

for cookie in cookie_list:
    driver.add_cookie(cookie)

driver.refresh()

# pass cloudflare
while True:
    try:
        time.sleep(5)
        if re.findall(
            " NULLSHIP.GG | MOST RELIABLE SHIPPING LABELS | STARTING PRICE $4 ",
            str(driver.page_source),
        ):
            break
        driver.switch_to.default_content()
        iframe = driver.find_element(
            by=By.XPATH,
            value="//iframe[@title='Widget containing a Cloudflare security challenge']",
        )
        driver.switch_to.frame(iframe)
        driver.find_element(by=By.XPATH, value="//input[@type='checkbox']").click()
    except Exception as e:
        print(e)

driver.execute_script(
    "document.querySelectorAll('.channel.channel-item.draggable-channel')[2].click()"
)
print(driver.page_source)

soup = BeautifulSoup(driver.page_source, features="html.parser")

message_tag = soup.find("div", attrs={"class": "messages"})

message_list = message_tag.findAll("div", attrs={"class": "entry"})


def get_info(link: str):
    temp_resp = session.get(link)
    print(temp_resp)
    return temp_resp


forum_link_list = []
for item in message_list:
    link = item.find("div", attrs={"class": "field cell-message"}).a["href"]
    forum_link_list.append(url + link)

result = []
# with concurrent.futures.ThreadPoolExecutor() as excutor:
#     threading_list = []
#     for link in forum_link_list:
#         threading_list.append(excutor.submit(get_info, link))
#     for thd in threading_list:
#         result.append(thd.result())

for link in forum_link_list:
    result.append(get_info(link))

print(result)
