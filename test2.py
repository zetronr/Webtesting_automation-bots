from bot_lib import Bot_driver

USERNAME = "user2"
PASSWORD = "123456"
BASE_URL = "http://172.25.116.2:33164"

#xpath list var: 

#side bar menu
home = "//em[@class='icon ni ni-home-fill']"
data_management = "//em[@class='icon ni ni-files-fill']"
user_management = "//em[@class='icon ni ni-account-setting-fill']"
campaign_setting = "//em[@class='icon ni ni-opt-alt-fill']"
application_setting = "//em[@class='icon ni ni-setting-alt-fill']"
product = "//em[@class='icon ni ni-package-fill']"
assignment = "//em[@class='icon ni ni-swap-alt-fill']"

#data management menu 
master_upload = "//div[@class='nk-menu-content menu-active']//li[1]//a[1]"
template_upload = "//span[normalize-space()='Template Upload']"
phone_list = "//span[normalize-space()='Phone List']"

#user management menu 
user_list = "//span[normalize-space()='Users List']"
role_configuration = "//span[normalize-space()='Role Configuration']"
login_activity_list = "//span[normalize-space()='Login Activity List']"

#campaign setting menu
campaign_list = "//span[normalize-space()='Campaign List']"
campaign_layout = "//span[normalize-space()='Campaign Layout']"
# Inisialisasi bot
bot = Bot_driver()

#agent elements:

workspace_button="//a[@class='btn btn-round float-right w-150px btn-primary justify-content-center']"
view_alldata_button = "//button[normalize-space()='View Data']"
addtodiallist_button = "//button[@class='btn btn-lg float-right btn-primary justify-content-center addDialList']"
goto_workspace_button = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/button[1]"

#popup recconect 
recconect_button = "//button[normalize-space()='Reconnect']"
exit_campaign = "//button[contains(text(),'Exit Campaign')]"

#call
call_button = "//tbody/tr[1]/td[4]/button[1]/span[1]"
hangup_button = "//div[@class='adminButtons']"

#form
connected = "//span[normalize-space()='Connected']"
contacted = "//p[normalize-space()='Customer reached. log the response!']"
agree = "//span[normalize-space()='Agree']"



try:
    bot.open_url(url=BASE_URL)
    
    # Login s
    if not bot.login(USERNAME, PASSWORD):
        raise Exception("Login gagal! Periksa kredensial atau sistem.")
    
    bot.click(xpath=workspace_button)
    bot.click(xpath=view_alldata_button)
    bot.delay(2)
    bot.click(xpath=addtodiallist_button)
    bot.delay(2)
    bot.click(xpath=goto_workspace_button)
    bot.delay(2)
    bot.click(xpath=connected)
    bot.delay(2)
    bot.click(xpath=contacted)
    bot.delay(2)
    bot.click(xpath=agree)
    
     
    bot.delay(3)

except Exception as e:
    print(f"Terjadi kesalahan: {e}")

