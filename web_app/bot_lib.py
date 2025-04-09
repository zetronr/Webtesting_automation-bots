from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import logging 
import os


class Bot_driver :
    def __init__(self, driver_path="chromedriver.exe"):
        options = Options()
        options.add_argument("--start-maximized") #fullscreen
        options.add_argument("--incognito")  
        self.service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=self.service, options=options)

    def open_url(self, url):
        self.base_url = url
        self.driver.get(f"{self.base_url}") 

    def logout(self):
        self.driver.get(f"{self.base_url}/logout") 

    def login(self, username, password):
        WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.NAME, "username"))
            ).send_keys(username)

        WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.NAME, "password"))
            ).send_keys(password + Keys.RETURN)
        return "PASS"
    
    def click(self,xpath:str,buttonname:str):
        WebDriverWait(self.driver,10).until(
                    EC.element_to_be_clickable((By.XPATH,xpath))
                        )
        click_button = self.driver.find_element(By.XPATH,xpath )
        self.driver.execute_script("arguments[0].click();", click_button)

    def input(self,xpath:str,input):
        WebDriverWait(self.driver,5).until(
                EC.presence_of_element_located((By.XPATH,xpath))
            ).send_keys(input)
        
    def select_dropdown(self,xpath:str,index:int):
            abc = self.driver.find_element(By.XPATH, xpath)
            bcd = Select(abc)
            bcd.select_by_visible_text(index)
        
    def insert_file(self, xpath: str, file: str):
    # Pastikan path file menjadi absolut
       absolute_file_path = os.path.abspath(file)
       print(f"Mengunggah file: {absolute_file_path} ke elemen {xpath}")

       input_file = WebDriverWait(self.driver, 3).until(
        EC.presence_of_element_located((By.XPATH, xpath))
          )
       input_file.send_keys(absolute_file_path)

    def delay(self, pause):
            time.sleep(pause)
    
    
         
        