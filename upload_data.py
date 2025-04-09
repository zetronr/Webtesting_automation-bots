import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import logging
from sele_bot import NTS_driver

# Konfigurasi Logging
log_filename = "upload_warnings.log"
logging.basicConfig(filename=log_filename, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Fungsi untuk memilih file
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xls;*.xlsx"), ("All Files", "*.*")])
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

# Fungsi untuk menjalankan otomatisasi Selenium
def run_selenium():
    username = username_entry.get()
    password = password_entry.get()
    file_template = file_entry.get()

    if not username or not password or not file_template:
        messagebox.showerror("Error", "Semua input harus diisi!")
        return

    def selenium_task():
        try:
            bot = NTS_driver()
            log_text.insert(tk.END, "[INFO] Memulai browser...\n")
            log_text.see(tk.END)

            bot.open_url("http://172.25.116.2:33164/login")
            log_text.insert(tk.END, "[INFO] Halaman login berhasil dibuka.\n")
            log_text.see(tk.END)

            login_success = bot.login(username, password)
            log_text.insert(tk.END, f"[INFO] Login: {login_success}.\n")
            log_text.see(tk.END)
            
            err_code = bot.navigate_to_upload_page("A")
            log_text.insert(tk.END, f"[INFO]Navigasi ke upload page: {err_code}.\n")
            log_text.see(tk.END)
            
            # bot.upload_tempfile(file_template)
            # log_text.insert(tk.END, f"[WARNING] File '{file_template}' berhasil di-upload tanpa memilih template!\n")
            # log_text.see(tk.END)

            name_template="check"
            bot.select_product_and_upload(file_template, template_name=name_template,product_index=2)
            log_text.insert(tk.END, f"[INFO] File '{file_template}' berhasil dipilih untuk di-upload.\n")
            log_text.see(tk.END)

            bot.navigate_to_master_upload()
            log_text.insert(tk.END, "[INFO] Navigasi ke Page Master berhasil.\n")
            log_text.see(tk.END)
            
            bot.upload_masters_nav()
            log_text.insert(tk.END, "[INFO] Navigasi ke Upload Master berhasil.\n")
            log_text.see(tk.END)
            
            bot.select_template(template_index=9)
            bot.select_campaign(campaign_index=8)
            #bot.upload_master_data(filemaster=file_template)

            bot.logout()
            log_text.insert(tk.END, "[INFO] Eksekusi selesai, Logout.\n")
            log_text.see(tk.END)

            bot.close_browser()
            log_text.insert(tk.END, "[INFO] Eksekusi selesai, browser ditutup.\n")
            log_text.see(tk.END)
        except Exception as e:
            log_text.insert(tk.END, f"[ERROR] {str(e)}\n")
            log_text.see(tk.END)
            logging.error(f"Terjadi kesalahan: {str(e)}")
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

    threading.Thread(target=selenium_task, daemon=True).start()

# ---------------------------- GUI ----------------------------
root = tk.Tk()
root.title("NTS-upload data test")
root.geometry("600x500")
root.resizable(False, False)

# Frame untuk Form Input
form_frame = tk.Frame(root, padx=20, pady=20)
form_frame.pack(padx=10, pady=10)

# Username
tk.Label(form_frame, text="Username:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
username_entry = tk.Entry(form_frame, width=40, font=("Arial", 12))
username_entry.grid(row=0, column=1, pady=5)

# Password
tk.Label(form_frame, text="Password:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
password_entry = tk.Entry(form_frame, width=40, font=("Arial", 12), show="*")
password_entry.grid(row=1, column=1, pady=5)

# File Template
tk.Label(form_frame, text="File Template:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
file_entry = tk.Entry(form_frame, width=30, font=("Arial", 12))
file_entry.grid(row=2, column=1, pady=5)
file_button = tk.Button(form_frame, text="Browse", command=select_file, font=("Arial", 12))
file_button.grid(row=2, column=2, padx=5)

# Tombol run Selenium
tk.Button(form_frame, text="Run", command=run_selenium, bg="green", fg="white", font=("Arial", 12), width=20).grid(row=3, column=0, columnspan=3, pady=20)

# Log Status
log_text = tk.Text(root, height=10, width=70, font=("Courier", 10), wrap="word")
log_text.pack()

root.mainloop()
