# import sqlite3
# import time
# from bot_lib import Bot_driver  


# class testCase_exc:  
#     def executeTc(self, testcase):
#         try: 
#             bot = Bot_driver()

#             def get_actions_from_db():
#                 conn = sqlite3.connect("bot_actions.db")  
#                 cursor = conn.cursor()
                
#                 cursor.execute("""SELECT  
#                         id, 
#                         xpath, 
#                         action_type, 
#                         insert_value, 
#                         url, 
#                         insert_file, 
#                         methode, 
#                         bytext, 
#                         byindex 
#                     FROM actions 
#                     ORDER BY id ASC""")
                
#                 actions = cursor.fetchall() 
#                 conn.close()
#                 return actions

#             actions = get_actions_from_db()
            
#             def get_target_id(testcase):
#                 conn = sqlite3.connect("bot_actions.db")  
#                 cursor = conn.cursor()
#                 query = f"SELECT action_id FROM {testcase}"
#                 cursor.execute(query)
#                 rows = cursor.fetchall()
#                 conn.close()

#                 # Ambil hanya angka id-nya dalam bentuk list
#                 return [row[0] for row in rows]

          
#             target_ids =  get_target_id(testcase)

          
#             filtered_actions = [action for action in actions if action[0] in target_ids]

#             for action in filtered_actions:
#                 action_id, xpath, action_type, insert_value, url, file_path, dropdown_method, text, index = action
                
#                 try:
#                     if url and url.strip():  
#                         if not url.startswith(("http://", "https://")):
#                             url = "http://" + url  
#                         print(f"[{action_id}] Membuka URL: {url}")
#                         bot.open_url(url)
#                         bot.delay(1)  
                    
#                     if xpath and xpath.strip(): 
#                         if action_type == "insert":
#                             print(f"[{action_id}] Memasukkan teks '{insert_value}' ke elemen {xpath}")
#                             bot.input(xpath, insert_value)

#                         elif action_type == "click":
#                             print(f"[{action_id}] Mengklik elemen {xpath}")
#                             bot.click(xpath, f"Button-{action_id}")

#                         elif action_type == "dropdown":
#                             print(f"[{action_id}] Memilih opsi dropdown: {text}")
#                             bot.select_dropdown(xpath, text) 

#                         elif action_type == "insert_file":
#                             print(f"[{action_id}] Mengunggah file: {file_path} ke elemen {xpath}")
#                             bot.insert_file(xpath, file_path)

#                         bot.delay(0.5)

#                 except Exception as e:
#                     print(f"[{action_id}] Gagal mengeksekusi aksi: {e}")

#             bot.delay(5)
#             bot.driver.quit()

#         except Exception as e:
#             print(f"Error saat menjalankan test case: {e}")

import sqlite3
import time
import os # Import os for os.path.exists
from bot_lib import Bot_driver

class testCase_exc:
    def executeTc(self, testcase):
        bot = None 

        try:
            bot = Bot_driver() 

           
            def get_actions_from_db():
                try:
                    with sqlite3.connect("bot_actions.db") as conn:
                        cursor = conn.cursor()
                        cursor.execute("""
                            SELECT
                                id,
                                xpath,
                                action_type,
                                insert_value,
                                url,
                                insert_file,
                                methode,
                                bytext,
                                byindex
                            FROM actions
                            ORDER BY id ASC
                        """)
                        actions = cursor.fetchall()
                        return actions
                except sqlite3.Error as e:
                    print(f"ERROR: Gagal mengambil aksi dari database: {e}")
                    return None 

          
            def get_target_id(testcase):
                try:
                    with sqlite3.connect("bot_actions.db") as conn:
                        cursor = conn.cursor()
                       
                        query = f"SELECT action_id FROM \"{testcase}\""
                        cursor.execute(query)
                        rows = cursor.fetchall()
                        return [row[0] for row in rows]
                except sqlite3.Error as e:
                    print(f"ERROR: Gagal mengambil target ID dari test case '{testcase}': {e}")
                    return None

            print(f"DEBUG: Memulai eksekusi test case: {testcase}")

            all_actions = get_actions_from_db()
            if all_actions is None:
                print("ERROR: Pengambilan aksi dari database gagal. Menghentikan eksekusi test case.")
                return False, "Pengambilan data aksi gagal." 

            target_ids = get_target_id(testcase)
            if target_ids is None:
                print(f"ERROR: Pengambilan ID target untuk test case '{testcase}' gagal. Menghentikan eksekusi test case.")
                return False, "Pengambilan ID test case gagal."
            # Filter aksi yang relevan dengan test case ini
            filtered_actions = [action for action in all_actions if action[0] in target_ids]

            if not filtered_actions:
                print(f"WARNING: Tidak ada aksi ditemukan untuk test case '{testcase}'.")
                return True, "Tidak ada aksi untuk dieksekusi." 

            for action in filtered_actions:
                action_id, xpath, action_type, insert_value, url, file_path, dropdown_method, text, index = action

                print(f"\n--- DEBUG: Mengeksekusi Aksi ID: {action_id} (Tipe: {action_type}) ---")
                
                try:
                    # Aksi Buka URL
                    if url and url.strip():
                        if not url.startswith(("http://", "https://")):
                            url = "http://" + url
                        print(f"[{action_id}] Membuka URL: {url}")
                        bot.open_url(url)
                        bot.delay(1)

                    
                    if xpath and xpath.strip():
                        if action_type == "insert":
                            print(f"[{action_id}] Memasukkan teks '{insert_value if insert_value else ''}' ke elemen {xpath}")
                            bot.input(xpath, insert_value)

                        elif action_type == "click":
                            print(f"[{action_id}] Mengklik elemen {xpath}")
                            bot.click(xpath, f"Button-{action_id}")

                        elif action_type == "dropdown":
                            print(f"[{action_id}] Memilih opsi dropdown: {text if text else ''} dari elemen {xpath}")
                            if dropdown_method == "by_text":
                                bot.select_dropdown(xpath, text=text)
                            elif dropdown_method == "by_index":
                                bot.select_dropdown(xpath, index=int(index) if index else 0)
                            else: # Default ke by_text jika tidak ditentukan
                                bot.select_dropdown(xpath, text=text)

                        elif action_type == "insert_file":
                            print(f"[{action_id}] Mengunggah file: {file_path if file_path else ''} ke elemen {xpath}")
                            if file_path and os.path.exists(file_path):
                                bot.insert_file(xpath, file_path)
                            else:
                                raise FileNotFoundError(f"File tidak ditemukan untuk diunggah: {file_path}")
                        
                        bot.delay(0.5)

                    print(f"[{action_id}] Aksi berhasil.")

                except Exception as e:
                    error_message = f"[{action_id}] GAGAL mengeksekusi aksi: {e}"
                    print(f"ERROR: {error_message}")
                    print("DEBUG: Menghentikan test case karena ada aksi yang gagal.")
                    return False, error_message # Mengembalikan False dan pesan error
            
            # Jika semua aksi berhasil dieksekusi tanpa return False
            print("\nDEBUG: Semua aksi dalam test case berhasil dieksekusi.")
            bot.delay(5) # Memberi waktu agar hasil terakhir terlihat atau untuk proses latar belakang
            return True, "Test case berhasil dieksekusi."

        except Exception as e:
            # Ini menangani error di luar loop aksi (misal, inisialisasi Bot_driver gagal)
            error_message = f"CRITICAL ERROR: Terjadi kesalahan saat menyiapkan atau menjalankan test case: {e}"
            print(f"ERROR: {error_message}")
            return False, error_message

        finally:
            # Pastikan driver browser ditutup meskipun ada error
            if bot and bot.driver:
                print("DEBUG: Menutup browser.")
                bot.driver.quit()