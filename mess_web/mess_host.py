import multiprocessing
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from dotenv import load_dotenv
import os



load_dotenv(override=True)
MESS_EMAIL = os.getenv('MESS_EMAIL')
MESS_PASS = os.getenv('MESS_PASS')
MESS_CHATNAME = os.getenv('MESS_CHATNAME')
MESS_SEND_MSG = os.getenv('MESS_SEND_MSG_TEXT')
MESS_URL = os.getenv('MESS_URL')

def subtract_msg(msg: str):
    msg = msg.split('\n')
    if(len(msg) == 1):
        return ""
    msg = [line for line in msg if MESS_SEND_MSG not in line]
    msg = '\n'.join(msg)
    return msg

def check_is_my_message(msg: str):
    my_msg_len = 1
    msg = msg.split('\n')
    if len(msg) == my_msg_len:
        return True
    else:
        return False

def main(users_queue: multiprocessing.Queue, bot_queue: multiprocessing.Queue):
    options = Options()
    options.add_experimental_option("detach", True)
    cService = webdriver.ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=cService, options=options)

    driver.get(MESS_URL)

    print("### ME$$ENGER STARTED ###")

    time.sleep(2)

    cookie_btn = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//button[@data-cookiebanner="accept_only_essential_button"]'))
    )
    cookie_btn.click()

    email = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'email'))
    )
    password = driver.find_element(by=By.ID, value='pass')

    email.send_keys(MESS_EMAIL)
    password.send_keys(MESS_PASS)
    password.send_keys(Keys.ENTER)

    selected_chat = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, f"//span[text()='{MESS_CHATNAME}']"))
    )
    selected_chat.click()

    time.sleep(2)

    chat_grid = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "(//div[@role='grid'])[last()]"))
    )

    last_chat_cell = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "(//div[@role='gridcell'])[last()-1]"))
    )

    textbox_div = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']"))
    )

    last_message = ""
    is_my_message = False

    #run recheck for every 5 seconds
    while True:
        last_chat_cell = driver.find_element(by=By.XPATH, value="(//div[@role='gridcell'])[last()-1]")
        subtracted_msg = subtract_msg(last_chat_cell.text)

        if subtracted_msg != last_message and subtracted_msg != "":
            last_message = subtracted_msg
            is_my_message = check_is_my_message(last_message)
        
            if is_my_message == False:
                print("=== SENDING ===")
                print(last_message)
                users_queue.put(last_message)

        if not bot_queue.empty():
            response = bot_queue.get()
            print("=== RECEIVED ===")
            print(response)
            textbox_div = driver.find_element(by=By.XPATH, value="//div[@role='textbox']")
            textbox_div.send_keys(response)
            textbox_div.send_keys(Keys.ENTER)

        time.sleep(5)

if __name__ == "__main__":
    main(None, None)

