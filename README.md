# 🔐 SQL Injection Learning Project (Flask-Based)

This project is a **Flask-based web application** designed **for educational purposes** to help beginners and security learners understand **how SQL injection attacks work** and how to **defend against them** using real-world prevention techniques like:

- Parameterized Queries
- Input Validation
- API Key Verification
- 2-Factor Authentication (2FA)
- Logging and Monitoring of Login Attempts

> ⚠️ **Disclaimer**: This project is intentionally vulnerable in places to demonstrate security flaws. It should **never** be deployed in a production environment. Use it only in controlled, local setups for learning purposes.

---

## 📚 Purpose

The goal of this app is to simulate both **vulnerable** and **secure** login mechanisms so that learners can:
- Perform basic SQL Injection attacks
- Learn to recognize insecure code
- Implement best practices to prevent exploitation
- Understand how API keys and 2FA enhance security

---

## 🛠 Project Features

### 1. 🐞 **SQL Injection Vulnerability (for demonstration)**
By default, the application uses **unsafe string concatenation** for SQL queries:
```python
query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
```
This query is vulnerable to SQL injection. Try:
```sql
Username: ' OR '1'='1
Password: anything
```
This will allow login without valid credentials (if protections are disabled).

---

### 2. 🛡️ **Parameterized Query (Safe Mode)**
To prevent SQL injection, you can enable secure code:
```python
query = "SELECT * FROM users WHERE username = ? AND password = ?"
cursor.execute(query, (username, password))
```
This binds user input safely without letting SQL commands be injected.

✅ Uncomment the secure block in `app.py` to activate this feature.

---

### 3. 🧼 **Input Validation**
You can activate input validation to ensure only alphanumeric usernames/passwords are allowed:
```python
if not re.match(r"^[a-zA-Z0-9_]{3,20}$", username):
    raise ValueError("Invalid username")
```
This reduces the chances of malicious characters being submitted.

✅ Uncomment the "input validation" section in `app.py`.

---

### 4. 🔑 **API Key Validation**
The app demonstrates how **API key-based validation** works between client and server.

In `index.html`, the form includes:
```html
<input type="hidden" name="api_key" value="my_secret_api_key_123">
```

On the server, `app.py` checks:
```python
if api_key != app.secret_key:
    return render_template("index.html", error="Invalid API key."), 401
```

You can simulate an **unauthorized request** using the `forgedindex.html` page, which omits the API key. The server will reject it.

---

### 5. 🔐 **2-Factor Authentication (2FA)**
An optional 2FA mechanism simulates sending a **6-digit code** to the user. The user must enter the code to complete login.

Flow:
1. After valid login, a code is generated and stored in `session['2fa_code']`.
2. The user is redirected to `/verify-2fa`.
3. If the code matches, login completes.

✅ Uncomment the 2FA logic in both the `/login` and `/verify-2fa` routes to enable it.

---

### 6. 📜 **Login Attempt Logging**
All login attempts (successful and failed) are recorded with:
- IP Address
- Username
- Password (for testing only; never log passwords in real apps)
- Success status
- Timestamp

You can see these logs using SQLite:

```bash
sqlite3 users.db
SELECT * FROM login_attempts;
```

This helps you simulate **monitoring and detection of brute-force or malicious login attempts**.

It also prints a warning if 3+ failed attempts come from the same IP within 10 minutes.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/sql-injection-demo.git
cd sql-injection-demo
```

### 2. Install Dependencies

```bash
pip install flask
```

### 3. Run the Application

```bash
python app.py
```

Visit: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 🧪 How to Test

### 🧨 Test SQL Injection
- Username: `' OR '1'='1`
- Password: anything

This will bypass login if parameterized query is **not** used.

---

### 🔏 Test API Key Protection
- Go to `/forged` page (`http://127.0.0.1:5000/forged`)
- Try to login — server will reject request due to **missing API key**.

---

### 🧪 Test 2FA
- Enable 2FA sections in `app.py`
- Login using valid credentials
- Enter the generated 6-digit code shown in the console

---

## 📂 Project Structure

```
├── app.py                 # Main Flask app
├── users.db               # SQLite database
├── templates/
│   ├── layout.html        # Shared layout
│   ├── index.html         # Login page
│   └── forgedindex.html   # Fake login form (for API key check)
├── static/
│   └── styles.css         # Styling (optional)
```

---

## 🧠 What You'll Learn

- How SQL Injection works and how to simulate it
- How parameterized queries and input validation block injection
- Why you should **never log raw passwords**
- How 2FA and API keys add layers of security
- Basic client-server trust concepts and request validation
- How to monitor suspicious login attempts from IPs

---

## 🧑‍💻 Author

**Sujjal Chapagain**  
Sophomore @ University of Southern Mississippi  
IBM Certified Software Engineer | Web Developer | Cybersecurity Enthusiast
