from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import random
import re
import datetime

app = Flask(__name__)
app.secret_key = 'my_secret_api_key_123'

# ---------- Initialize database --------------------------------------------------------------------------------------------------
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    cursor.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'admin123')")
    cursor.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (2, 'user', 'user123')")

    # Log table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            username TEXT,
            password TEXT,
            success INTEGER,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()

#-----uncomment the line till {init_db()} for creating a database and putting login attemps information------------------------------------------------------
def log_login_attempt(ip, username, password, success):
    timestamp = datetime.datetime.now().isoformat()
    try:
        with sqlite3.connect("users.db", timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO login_attempts (ip, username, password, success, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (ip, username, password, int(success), timestamp))
            conn.commit()
    except sqlite3.OperationalError as e:
        print(f"[ERROR] Failed to log login attempt due to DB lock: {e}")

def get_recent_failed_attempts(ip, minutes=10):
    time_threshold = (datetime.datetime.now() - datetime.timedelta(minutes=minutes)).isoformat()
    try:
        with sqlite3.connect("users.db", timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) FROM login_attempts
                WHERE ip = ? AND success = 0 AND timestamp > ?
            ''', (ip, time_threshold))
            count = cursor.fetchone()[0]
            return count
    except sqlite3.OperationalError as e:
        print(f"[ERROR] Failed to retrieve login attempts: {e}")
        return 0

init_db()
#--------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        api_key = request.form['api_key']
        username = request.form['username']
        password = request.form['password']
        ip = request.remote_addr

#---uncomment three lines below for API check(note that it is unsafe to directly put API key in you html page as it can be inspected from browser. It is only to understand how the serers validate API keys------------------------------------------------------------------
        if api_key != app.secret_key:
            error = "Invalid API key."
            return render_template("index.html", error=error), 401
#---------------------------------------------------------------------------------------------------------------------------------------------------

#-------uncomment four lines below for enabling input validation-------------------------------------------------------------
        # if not re.match(r"^[a-zA-Z0-9_]{3,20}$", username):
        #     raise ValueError("Invalid username")
        # if not re.match(r"^[a-zA-Z0-9_]{3,20}$", password):
        #     raise ValueError("Invalid password")
#--------------------------------------------------------------------------------------------------------------------------------

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

#----------------------uncomment two lines below for Secure version (commented out for comparison)----------------------------------------------
        # query = "SELECT * FROM users WHERE username = ? AND password = ?"
        # cursor.execute(query, (username, password))
#------------------------------------------------------------------------------------------------------------------------------------------------

#----------------------uncomment two lines below for unecure version (commented out for comparison)----------------------------------------------
        query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
        cursor.execute(query)
#--------------------------------------------------------------------------------------------------------------------------------------------------

        user = cursor.fetchone()
        conn.close()

#------------------------uncomment line below for recording login attempts(dont forget to uncomment other parts for recording login ttempts)-----------------------------------------------------------------------
        log_login_attempt(ip, username, password, bool(user))
#--------------------------------------------------------------------------------------------------------------------------------------------------


        if user:
            session['temp_user'] = username

# ----------------------uncomment four lines below to Begin 2FA logic (dont forget to uncomment other parts for 2FA logic) ------------------------------------------------------------------------
            # code = str(random.randint(100000, 999999))  # Generate 6-digit code
            # session['2fa_code'] = code
            # print(f"Sending code to user's phone: {code}")
            # return redirect(url_for('verify_2fa'))
#------------------------------- End 2FA logic ----------------------------------------------------------------------------------------------------

            return f"Welcome, {user[1]}! You're logged in."

#-----------------------uncomment five lines below for recording login attempts(dont forget to uncomment other parts for recording login ttempts)-
        failed_attempts = get_recent_failed_attempts(ip)
        print(f"Failed login attempts from IP {ip}: {failed_attempts}")
        if failed_attempts >= 3:
            print(f"[ALERT] More than 3 failed login attempts detected from IP: {ip}")
            error = "Warning: More than 3 failed login attempts from your IP!"
#-------------------------------------------------------------------------------------------------------------------------------------------

        else:
            error = "Invalid credentials. Try again."

    return render_template("index.html", error=error)

# ----------------------uncomment 16 lines below to Begin 2FA logic (dont forget to uncomment other parts for 2FA logic) -----
@app.route('/verify-2fa', methods=['GET', 'POST'])
# def verify_2fa():
#     if request.method == 'POST':
#         input_code = request.form['code']
#         if input_code == session.get('2fa_code'):
#             username = session.pop('temp_user', None)
#             session.pop('2fa_code', None)
#             return f"Welcome, {username}! 2FA complete and you're logged in."
#         return "Invalid verification code."
#     return '''
#         <h3>2FA Verification</h3>
#         <form method="post">
#             <label>Enter the code sent to your phone:</label>
#             <input type="text" name="code" required>
#             <input type="submit" value="Verify">
#         </form>
#      '''

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/forged')
def forged():
    return render_template("forgedindex.html")

if __name__ == '__main__':
    app.run(debug=True)