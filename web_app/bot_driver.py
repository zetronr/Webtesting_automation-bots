import sqlite3
import time
from bot_lib import Bot_driver  


class testCase_exc:  
    def executeTc(self, testcase):
        try: 
            bot = Bot_driver()

            def get_actions_from_db():
                conn = sqlite3.connect("bot_actions.db")  
                cursor = conn.cursor()
                
                cursor.execute("""SELECT  
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
                    ORDER BY id ASC""")
                
                actions = cursor.fetchall() 
                conn.close()
                return actions

            actions = get_actions_from_db()
            
            def get_target_id(testcase):
                conn = sqlite3.connect("bot_actions.db")  
                cursor = conn.cursor()
                query = f"SELECT action_id FROM {testcase}"
                cursor.execute(query)
                rows = cursor.fetchall()
                conn.close()

                # Ambil hanya angka id-nya dalam bentuk list
                return [row[0] for row in rows]

          
            target_ids =  get_target_id(testcase)

          
            filtered_actions = [action for action in actions if action[0] in target_ids]

            for action in filtered_actions:
                action_id, xpath, action_type, insert_value, url, file_path, dropdown_method, text, index = action
                
                try:
                    if url and url.strip():  
                        if not url.startswith(("http://", "https://")):
                            url = "http://" + url  
                        print(f"[{action_id}] Membuka URL: {url}")
                        bot.open_url(url)
                        bot.delay(1)  
                    
                    if xpath and xpath.strip(): 
                        if action_type == "insert":
                            print(f"[{action_id}] Memasukkan teks '{insert_value}' ke elemen {xpath}")
                            bot.input(xpath, insert_value)

                        elif action_type == "click":
                            print(f"[{action_id}] Mengklik elemen {xpath}")
                            bot.click(xpath, f"Button-{action_id}")

                        elif action_type == "dropdown":
                            print(f"[{action_id}] Memilih opsi dropdown: {text}")
                            bot.select_dropdown(xpath, text) 

                        elif action_type == "insert_file":
                            print(f"[{action_id}] Mengunggah file: {file_path} ke elemen {xpath}")
                            bot.insert_file(xpath, file_path)

                        bot.delay(0.5)

                except Exception as e:
                    print(f"[{action_id}] Gagal mengeksekusi aksi: {e}")

            bot.delay(5)
            bot.driver.quit()

        except Exception as e:
            print(f"Error saat menjalankan test case: {e}")
