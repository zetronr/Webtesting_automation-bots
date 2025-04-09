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

# Konfigurasi logging untuk mencatat warning ke file
log_filename = "upload_warnings.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

class NTS_driver:
    def __init__(self, driver_path="chromedriver.exe"):
        """Inisialisasi Selenium dengan WebDriver"""
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--incognito")  # Membuka dalam mode fullscreen
        self.service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=self.service, options=options)

    def open_url(self, url):
        """Membuka halaman URL tertentu"""
        self.driver.get(url)

    def login(self, username, password):
        """Login ke dalam sistem"""
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.NAME, "username"))
            ).send_keys(username)

            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.NAME, "password"))
            ).send_keys(password + Keys.RETURN)
            return "PASS"
            
        except Exception as e:
            logging.warning(f"Login gagal")
            return f"FAIL {e}"
    def navigate_to_upload_page(self, err_code):
        """Navigasi ke halaman Template Upload"""
        try:
            WebDriverWait(self.driver, 1).until(
                EC.presence_of_element_located((By.XPATH, "//em[@class='icon ni ni-files-fill']"))
            )
            icon_button = self.driver.find_element(By.XPATH, "//em[@class='icon ni ni-files-fill']")
            self.driver.execute_script("arguments[0].click();", icon_button)

            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Template Upload']"))
            ).click()
          
            return "PASS"
        except Exception as e:
            logging.warning(f"Gagal navigasi ke halaman upload: {e}")
            return "FAIL"

    def upload_tempfile(self, file_path):
        """Upload file template tanpa memilih produk"""
        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='upload_template']"))
            ).send_keys(file_path)

            warning_message = f"File '{file_path}' berhasil di-upload tanpa memilih template!"
            logging.warning(warning_message)
        except Exception as e:
            logging.warning(f"Gagal upload file: {e}")

    def select_product_and_upload(self,file_path,template_name,product_index):
        """Upload file setelah memilih produk dan memberikan nama template"""
        try:
            dropdown = self.driver.find_elements(By.TAG_NAME, "option")
            # if len(dropdown) > 2:
            dropdown[product_index].click()  
            # Pilih produk tertentu
            # else:
                # logging.warning("Dropdown produk tidak ditemukan atau memiliki elemen kurang dari 3.")

            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='upload_template']"))
            ).send_keys(file_path)

            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='templatename']"))
            ).send_keys(template_name + Keys.RETURN)
            
            #sleep buat liat 
            #time.sleep(5)    
            # WebDriverWait(self.driver, 5).until(
            #     EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Submit']"))
            # ).click()
        except Exception as e:
            logging.warning(f"Gagal upload dengan produk: {e}")

    def navigate_to_master_upload(self):
        """Navigasi ke halaman Master Upload"""
        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Master Upload']"))
            ).click()
        except Exception as e:
            logging.warning(f"Gagal navigasi ke Master Upload: {e}")

 #button upload master
    def upload_masters_nav(self):
        try:
            WebDriverWait(self.driver, 1).until(
                EC.presence_of_element_located((By.XPATH, "//a[@class='btn btn-icon btn-primary d-md-none']"))
            )
            upload_button = self.driver.find_element(By.XPATH, "//a[@class='btn btn-icon btn-primary d-md-none']")
            self.driver.execute_script("arguments[0].click();", upload_button)

           
        except Exception as e:
            logging.warning(f"Gagal navigasi ke halaman upload master: {e}")
# upload file master 
  # insert file 
    def upload_master_data(self, filemaster):
        try: 
           WebDriverWait(self.driver,3).until(
               EC.presence_of_element_located((By.XPATH, "//input[@id='file_upload']"))
           ).send_keys(filemaster)

        except Exception as e:
            logging.warning(f"Gagal Upload File Master: {e}")

  # memilih campaign 
    def select_campaign(self, campaign_index):
        try: 
           abc = self.driver.find_element(By.ID, "campaign_id")
           bcd = Select(abc)
           bcd.select_by_index(campaign_index)
           time.sleep(5)
        except Exception as e:
            logging.warning(f"Gagal memilih campaign: {e}")   
             

  # memilih template 
    def select_template(self, template_index):
        try: 
           cde = self.driver.find_element(By.ID, "xtpl")
           efg = Select(cde)
           efg.select_by_index(template_index)
           time.sleep(5)
        except Exception as e:
            logging.warning(f"Gagal memilih template: {e}")  
  # menu user 
    def user_button(self,err_code):
        try: 
            WebDriverWait(self.driver,5).until(
                EC.presence_of_element_located((By.XPATH, "//em[@class='icon ni ni-account-setting-fill']"))
            ).click()
            return "PASS"
        except Exception as e:
            logging.warning(f"Gagal navigasi ke halaman user: {e}")
            return "FAIL"
        
#Product 
   #click menu product 
    def click_product(self):
        try:
            WebDriverWait(self.driver,5).until(
                EC.presence_of_element_located((By.XPATH,"//em[@class='icon ni ni-package-fill']"))
            )

            click_button = self.driver.find_element(By.XPATH,"//em[@class='icon ni ni-package-fill']" )
            self.driver.execute_script("arguments[0].click();", click_button)
        except Exception as e:
            logging.warning(f"Gagal click product: {e}")
    #click product list 
    def click_product_list(self):
        try: 
            xpath = "//span[normalize-space()='Product List']"
            WebDriverWait(self.driver,5).until(
                EC.presence_of_element_located((By.XPATH,xpath))
            )
            click_button = self.driver.find_element(By.XPATH,xpath )
            self.driver.execute_script("arguments[0].click();", click_button)
        except Exception as e:
            logging.warning(f"Gagal click product list: {e}")

    #click add product
    def click_add_product(self):
        xpath = "//span[normalize-space()='Add Product']"
        try:
            WebDriverWait(self.driver,5).until(
                EC.presence_of_element_located((By.XPATH,xpath))
            )
            click_button = self.driver.find_element(By.XPATH,xpath )
            self.driver.execute_script("arguments[0].click();", click_button)
        except Exception as e:
            logging.warning(f"Gagal click add product: {e}")

    def delay(self, pause):
        try:
            time.sleep(pause)
        except Exception as e:
            logging.warning(f"Gagal pause : {e}")
    
    # create new product 
    def create_new_product(self,product_code, product_name, product_description, isactive:bool):
        try:
            WebDriverWait(self.driver,5).until(
                EC.presence_of_element_located((By.XPATH,"//input[@id='code']"))
            ).send_keys(product_code)

            WebDriverWait(self.driver,5).until(
                EC.presence_of_element_located((By.XPATH,"//input[@id='name']"))
            ).send_keys(product_name)

            WebDriverWait(self.driver,5).until(
                EC.presence_of_element_located((By.XPATH,"//input[@id='description']"))
            ).send_keys(product_description)

            WebDriverWait(self.driver,5).until(
                EC.presence_of_element_located((By.XPATH,"//label[@class='custom-control-label']"))
            )
            if isactive:
                click_button = self.driver.find_element(By.XPATH,"//label[@class='custom-control-label']" )
                self.driver.execute_script("arguments[0].click();", click_button)


            WebDriverWait(self.driver,5).until(
                    EC.presence_of_element_located((By.XPATH,"//button[@type='submit']"))
                        )
            click_button = self.driver.find_element(By.XPATH,"//button[@type='submit']" )
            self.driver.execute_script("arguments[0].click();", click_button)   
            

        except Exception as e:
            logging.warning(f"Gagal add new product: {e}")

      
#app settings 
    def click_app_setting(self):
        try:
            xpath = ""
            WebDriverWait(self.driver,5).until(
                    EC.presence_of_element_located((By.XPATH,xpath))
                        )
            click_button = self.driver.find_element(By.XPATH,xpath )
            self.driver.execute_script("arguments[0].click();", click_button)
        except Exception as e:
                   logging.warning(f"Gagal click app setting : {e}")

    def click(self,xpath:str,buttonname:str):
        try:
          
          WebDriverWait(self.driver,10).until(
                    EC.element_to_be_clickable((By.XPATH,xpath))
                        )
          click_button = self.driver.find_element(By.XPATH,xpath )
          self.driver.execute_script("arguments[0].click();", click_button)
        except Exception as e:
                   logging.warning(f"Gagal click: {e}")

    def input(self,xpath:str,input):
        try:
             WebDriverWait(self.driver,5).until(
                EC.presence_of_element_located((By.XPATH,xpath))
            ).send_keys(input)
        except Exception as e:
                   logging.warning(f"Gagal input: {e}")

    def select_dropdown(self,xpath:str,index:int):
        try: 
            abc = self.driver.find_element(By.XPATH, xpath)
            bcd = Select(abc)
            bcd.select_by_visible_text(index)
        except Exception as e:
                   logging.warning(f"Gagal select index: {e}")

    def insert_file(self,xpath:str,file:str):
        try: 
             input_file = WebDriverWait(self.driver,3).until(
               EC.presence_of_element_located((By.XPATH, xpath))
           )
             input_file.send_keys(file)
        except Exception as e:
                   logging.warning(f"Gagal memasukan file: {e}")

    

# log out 
    def logout(self):
        try:
            WebDriverWait(self.driver,5).until(
                EC.presence_of_element_located((By.XPATH, "//em[@class='icon ni ni-home-fill']"))
            ).click()

            WebDriverWait(self.driver,5).until(
                EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Statistik']"))
            ).click()
            
            WebDriverWait(self.driver,5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='user-name dropdown-indicator']"))
            ).click() 
            WebDriverWait(self.driver,5).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Sign')]"))
            ).click() 

            time.sleep(5)
        except Exception as e:
            logging.warning(f"Gagal Log out: {e}")

    def close_browser(self):
        """Menutup browser"""
        time.sleep(5)
        self.driver.quit()
