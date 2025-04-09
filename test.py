from sele_bot import NTS_driver  # Pastikan sele_bot sudah terinstal dan tersedia

# Konfigurasi kredensial
USERNAME = "admin"
PASSWORD = "123456"
BASE_URL = "http://172.25.116.2:33164"

# Inisialisasi bot
bot = NTS_driver()

try:
    # Buka halaman login
    bot.open_url(f"{BASE_URL}/login")

    # Login dengan kredensial
    if not bot.login(USERNAME, PASSWORD):
        raise Exception("Login gagal! Periksa kredensial atau sistem.")
    
    # Navigasi ke halaman produk
    bot.click_product()
    bot.click_product_list()
    bot.click_add_product()

    # Menambahkan produk baru
    new_product = bot.create_new_product(
        product_code="AAA",
        product_name="zzzz",
        product_description="test",
        isactive=0
    )
    bot.delay(3)
    bot.click(
        xpath="//a[normalize-space()='3']",
        buttonname="Page 3"
    )
    bot.delay(3)
    bot.click(
        xpath="//a[normalize-space()='2']",
        buttonname="Page 2"
    )
    bot.delay(3)
    bot.click(
        xpath="//a[normalize-space()='4']",
        buttonname="Page 4"
    )
    
except Exception as e:
    print(f"Terjadi kesalahan: {e}")

finally:
    # Logout dan tutup bot
    bot.logout()
    print("Bot telah logout.")
