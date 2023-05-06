import codecs
import time

from selenium.webdriver.common.by import By

# from selenium.webdriver.support import expected_conditions as EC
from utils.BaseDrive import BaseDrive


def save(text: str):
    with codecs.open("a.html", mode="w") as f:
        f.write(text)
        f.close()


url = "https://www.nulled.to/"
id = "atlasd"
psw = "@@Tata123"

driver = BaseDrive().driver
driver.get(url)
time.sleep(5)

# pass Cloudfare

driver.performClick(By.XPATH, "//a[@id='sign_in']")
time.sleep(0.5)
driver.performSendKyes(By.XPATH, "//input[@id='ips_username']", id)
time.sleep(0.5)
driver.performSendKyes(By.XPATH, "//input[@id='ips_password']", psw)
time.sleep(0.5)
iframe = driver.driver.find_element(By.XPATH, "//iframe[@title='reCAPTCHA']")

driver.driver.switch_to.frame(iframe)

driver.performClick(By.XPATH, "//div[@class='recaptcha-checkbox-border']")
soup = driver.getSoup()

recaptcha_token = soup.find("input", attrs={"id": "recaptcha-token"})["value"]

driver.driver.switch_to.default_content()


driver.driver.execute_script(
    f'document.getElementById("g-recaptcha-response").value = "{recaptcha_token}";'
)

iframe = driver.driver.find_element(
    By.XPATH, "//iframe[@title='recaptcha challenge expires in two minutes']"
)
driver.driver.switch_to.frame(iframe)

driver.performClick(By.XPATH, "//button[@id='recaptcha-verify-button']")
