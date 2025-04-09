from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def create_testcase_table(tc_name):
    conn = sqlite3.connect("bot_actions.db")
    cursor = conn.cursor()

    # Table name must be sanitized if input comes from user
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

def get_actionname():
    conn = sqlite3.connect("bot_actions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, action_name FROM actions")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_db_connection():
    conn = sqlite3.connect("bot_actions.db")  # Gunakan bot_actions.db di sini juga
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/action-list')
def list_actions():
    conn = get_db_connection()
    actions = conn.execute("SELECT * FROM actions").fetchall()
    conn.close()
    return render_template('list_action.html', actions=actions)

@app.route('/testcase-list')
def test_case():
    return render_template('testcase.html')

@app.route('/newtestcase')
def newtest_case():
    data=get_actionname()
    return render_template('newtestcase.html',actions = data)


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
    action_name = request.form.get("action_name")
    xpath = request.form.get("xpath")
    action_type = request.form.get("action_type")
    url = request.form.get("url")
    insert_value = request.form.get("insert", None)
    methode = request.form.get("methode", None)
    bytext = request.form.get("bytext", None)
    byindex = request.form.get("byindex", None)

    file = request.files.get("insertfile")
    file_path = None

    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)  # Simpan path file
        file.save(file_path)  # Simpan file di folder uploads

    try:
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO actions (action_name, xpath, action_type, url, insert_value, insert_file, methode, bytext, byindex) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (action_name, xpath, action_type, url, insert_value, file_path, methode, bytext, byindex))
        conn.commit()
        conn.close()

        return jsonify({"message": "Data berhasil disimpan ke database!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Route untuk Mengunduh File dari Folder
@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

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

if __name__ == "__main__":
    app.run(debug=True)
