from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
from bot_driver import testCase_exc
import tkinter as tk
import webbrowser
import sqlite3
import os
import json
import re

# import tensorflow as tf

# interpreter = tf.lite.Interpreter(
#     model_path="model.tflite",
#     experimental_delegates=[]
# )
# interpreter.allocate_tensors()

tc = testCase_exc

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def create_testcase_table(tc_name):
    conn = sqlite3.connect("bot_actions.db")
    cursor = conn.cursor()

    
    query = f'''
        CREATE TABLE IF NOT EXISTS "{tc_name}" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_id INTEGER NOT NULL,
            FOREIGN KEY (action_id) REFERENCES actions(id)
        )
    '''
    cursor.execute(query)
    conn.commit()
    conn.close()

def insert_to_testcase(tc_name, action_id):
    conn = sqlite3.connect("bot_actions.db")
    cursor = conn.cursor()

    cursor.execute(f'INSERT INTO "{tc_name}" (action_id) VALUES (?)', (action_id,))
    conn.commit()
    conn.close()
    

def get_actions():
    conn = sqlite3.connect("bot_actions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM actions")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_testcase():
    conn = sqlite3.connect("bot_actions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'Tc\_%' ESCAPE '\\';")
    tables = cursor.fetchall()
    conn.close()
    return tables

def get_actionname():
    conn = sqlite3.connect("bot_actions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, action_name FROM actions")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_db_connection():
    conn = sqlite3.connect("bot_actions.db")  
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/action-list')
def list_actions():
    print("route action list clicked")
    conn = get_db_connection()
    actions = conn.execute("SELECT * FROM actions").fetchall()
    conn.close()
    return render_template('list_action.html', actions=actions)

@app.route('/testcase-list')
def test_case():
    dataTc = get_testcase()
    return render_template('testcase.html',actions = dataTc )

@app.route('/newtestcase')
def newtest_case():
    data=get_actionname()
    return render_template('newtestcase.html',actions = data)



@app.route('/delete-testcase/<tableName>',methods=["POST"])
def delete_testcase(tableName):
    try: 
        conn = sqlite3.connect("bot_actions.db")
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS [{tableName}]")  # aman terhadap nama dengan spasi/karakter khusus
        conn.commit()
        conn.close()
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))

# @app.route('/execute-testcase/<testcaseName>',methods=["POST"])
# def executeTestcase(testcaseName):
#     try:
#         tc.executeTc(self=tc,testcase=testcaseName)
#         return jsonify(success = True)
#     except Exception as e:
#         return str(e), 500
    


@app.route('/execute-testcase/<testcaseName>',methods=["POST"])
def executeTestcase(testcaseName):
    print(f"DEBUG: Menerima permintaan untuk mengeksekusi test case: {testcaseName}")
    try:
        
        success, message = tc.executeTc(self=tc,testcase=testcaseName)

        if success:
            print(f"DEBUG: Eksekusi test case '{testcaseName}' berhasil. Pesan: {message}")
            return jsonify(success=True, message=message)
        else:
            print(f"ERROR: Eksekusi test case '{testcaseName}' GAGAL. Pesan: {message}")
            return jsonify(success=False, error=message), 500 
    except Exception as e:
       
        print(f"CRITICAL ERROR di Flask route: {e}")
        return jsonify(success=False, error=f"Kesalahan internal server: {str(e)}"), 500


@app.route("/delete-action/<int:action_id>", methods=["POST"])
def delete_action(action_id):
    try:
        conn = sqlite3.connect("bot_actions.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM actions WHERE id = ?", (action_id,))
        conn.commit()
        conn.close()
        
        return jsonify({"message": "Action deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/add-action")
def index():
    return render_template("index.html")

@app.route("/logsaction")
def logs():
    return render_template("aduh.html")

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route("/dbdashboard")
def show_actions():
    data = get_actions()
    return render_template("table.html", actions=data)

@app.route("/submit_testcase", methods=["POST"])
def submit_testcase():
    data = request.get_json()
      
    if not data:
        return jsonify({"status": "error", "message": "Data JSON tidak ditemukan."}), 400

    tc_name = data.get("testcase_name")
    actions = data.get("actions", [])
    testcasedb = "tc_"+tc_name
    if not tc_name or len(actions) == 0:
        return jsonify({"status": "error", "message": "Nama test case dan minimal satu aksi diperlukan."}), 400

    # Buat tabel baru sesuai nama test case
    create_testcase_table(testcasedb)

    inserted = []
    for action in actions:
        try:
            action_id = int(action["id"])
            insert_to_testcase(testcasedb, action_id)
            inserted.append(action_id)
        except Exception as e:
            print(f"Gagal insert action_id {action.get('id')}: {e}")

    return jsonify({
        "status": "success",
        "message": f"Test case '{tc_name}' berhasil disimpan!",
        "inserted_action_ids": inserted
    }), 200


@app.route("/submit", methods=["POST"])
def submit():
    # Print all form data received
    print("--- DEBUG: /submit POST Request Received ---")
    print(f"DEBUG: Form Data: {request.form}")
    print(f"DEBUG: Files Data: {request.files}")

    action_name = request.form.get("action_name")
    xpath = request.form.get("xpath")
    action_type = request.form.get("action_type")
    url = request.form.get("url")
    insert_value = request.form.get("insert", None)
    methode = request.form.get("methode", None)
    bytext = request.form.get("bytext", None)
    byindex = request.form.get("byindex", None)

    # Print extracted values
    print(f"DEBUG: action_name: {action_name}")
    print(f"DEBUG: xpath: {xpath}")
    print(f"DEBUG: action_type: {action_type}")
    print(f"DEBUG: url: {url}")
    print(f"DEBUG: insert_value: {insert_value}")
    print(f"DEBUG: methode: {methode}")
    print(f"DEBUG: bytext: {bytext}")
    print(f"DEBUG: byindex: {byindex}")

    file = request.files.get("insertfile")
    file_path = None

    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        try:
            file.save(file_path)
            print(f"DEBUG: File saved successfully to: {file_path}")
        except Exception as e:
            print(f"ERROR: Failed to save file: {e}")
            return jsonify({"error": f"Gagal menyimpan file: {str(e)}"}), 500
    else:
        print("DEBUG: No file uploaded.")

    try:
        conn = get_db_connection()
        # Print the values being inserted
        print(f"DEBUG: Attempting to insert into 'actions' table with values:")
        print(f"DEBUG: action_name={action_name}, xpath={xpath}, action_type={action_type}, url={url}, insert_value={insert_value}, insert_file={file_path}, methode={methode}, bytext={bytext}, byindex={byindex}")

        conn.execute("""
            INSERT INTO actions (action_name, xpath, action_type, url, insert_value, insert_file, methode, bytext, byindex) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (action_name, xpath, action_type, url, insert_value, file_path, methode, bytext, byindex))
        conn.commit()
        conn.close()
        print("DEBUG: Data successfully committed to database.")

        return jsonify({"message": "Data berhasil disimpan ke database!"})

    except sqlite3.Error as e: # Catch specific SQLite errors
        print(f"ERROR: SQLite Database Error: {e}")
        return jsonify({"error": f"Kesalahan database: {str(e)}"}), 500
    except Exception as e: # Catch any other unexpected errors
        print(f"ERROR: Unexpected Error during submission: {e}")
        return jsonify({"error": f"Terjadi kesalahan tak terduga: {str(e)}"}), 500

#Route untuk Mengunduh File dari Folder
@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route("/edit-testcase/<tableName>", methods = ["GET","POST"])
def edit_testcase(tableName):
    conn = get_db_connection()
    cursor = conn.cursor()

    data = get_actionname()

    try:
        cursor.execute(f'SELECT action_id FROM "{tableName}"')
        rows = cursor.fetchall()
        actionIdList = [row["action_id"] for row in rows]
  # List of selected action IDs
    except Exception as e:
        conn.close()
        return f"Error membaca tabel {tableName}: {e}", 500

        conn.close()

    return render_template(
    "edit_testcase.html",
    tcName=tableName,
    actions=data
)

@app.route("/table-data/<tableName>",methods = ["GET"])
def send_tabledata(tableName):
   conn = get_db_connection()
   cursor = conn.cursor() 
   try:
        cursor.execute(f'SELECT action_id FROM "{tableName}"')
        rows = cursor.fetchall()
        actionIdList = [row["action_id"] for row in rows]
        detailedActions = [getActioninfo(action_id) for action_id in actionIdList]
 
   except Exception as e:
        conn.close()
        return f"Error membaca tabel {tableName}: {e}", 500
        conn.close()

   return jsonify(detailedActions)



    
def getActioninfo(actionID):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM actions WHERE id = ?", (actionID,))   
    row = cursor.fetchone()
    conn.close() 

    if row:
        
        return {
            "id": row["id"],
            "name": row["action_name"],
            "xpath": row["xpath"],
            "type": row["action_type"],
            "url": row["url"],
            "inset_value": row["insert_value"],
            "insert_file": row["insert_file"],
            "methode": row["methode"],
            "bytext": row["bytext"],
            "byindex": row["byindex"]
        }
    else:
        return None
   

@app.route("/edit-action/<int:action_id>", methods=["GET", "POST"])
def edit_action(action_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == "POST":
        action_name = request.form.get("action_name")
        xpath = request.form.get("xpath")
        action_type = request.form.get("action_type")
        url = request.form.get("url", None)
        insert_value = request.form.get("insert", None)
        methode = request.form.get("methode", None)
        bytext = request.form.get("bytext", None)
        byindex = request.form.get("byindex", None)

        file = request.files.get("insertfile")
        insert_file = file.filename if file else None
        
        cursor.execute("""
            UPDATE actions
            SET action_name = ?, xpath = ?, action_type = ?, url = ?, insert_value = ?, insert_file = ?, methode = ?, bytext = ?, byindex = ?
            WHERE id = ?
        """, (action_name, xpath, action_type, url, insert_value, insert_file, methode, bytext, byindex, action_id))

        conn.commit()
        conn.close()
        return redirect(url_for("list_actions"))
    
    cursor.execute("SELECT * FROM actions WHERE id = ?", (action_id,))
    action = cursor.fetchone()
    conn.close()
    
    if action:
        return render_template("edit_action.html", action=action)
    else:
        return jsonify({"error": "Action not found"}), 404
    
@app.route('/update-testcase/<table_name>', methods=['POST'])
def update_testcase(table_name):
    data = request.get_json()
    actions = data.get('actions', [])

    if not re.match(r'^[a-zA-Z0-9_]+$', table_name):
        return jsonify({"success": False, "message": "Invalid table name"}), 400

    try:
        with sqlite3.connect("bot_actions.db", timeout=10) as conn:
            cursor = conn.cursor()
            cursor.execute(f'DELETE FROM "{table_name}"')

            for action in actions:
                cursor.execute(f'''
                    INSERT INTO "{table_name}" (action_id)
                    VALUES (?)
                ''', (action['id'],))

            conn.commit()

        return jsonify({"success": True, "message": "Test case updated"})

    except sqlite3.OperationalError as e:
        if "database is locked" in str(e):
            return jsonify({"success": False, "message": "Database is currently locked. Please try again shortly."}), 500
        return jsonify({"success": False, "message": f"Database error: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"success": False, "message": f"Unexpected error: {str(e)}"}), 500
    
def open_url():
    webbrowser.open("http://127.0.0.1:5000/add-action")  



if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)




