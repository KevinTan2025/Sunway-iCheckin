import requests
from bs4 import BeautifulSoup
import urllib3
import csv
import random
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LOGIN_URL = "https://izone.sunway.edu.my/login"
CHECKIN_URL = "https://izone.sunway.edu.my/icheckin/iCheckinNowWithCode"
PROFILE_URL = "https://izone.sunway.edu.my/student/myProfile"

def load_user_agents():
    user_agents = []
    ua_file = os.path.join(os.path.dirname(__file__), 'ua.csv')
    try:
        with open(ua_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                if row and row[0].strip():
                    user_agents.append(row[0].strip())
    except Exception as e:
        print(f"Failed to read user agent file: {e}")
        user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"]
    return user_agents

def load_users():
    users = []
    users_file = os.path.join(os.path.dirname(__file__), 'users.csv')
    try:
        print(f"Reading user file: {users_file}")
        with open(users_file, 'r') as csvfile:
            content = csvfile.read()
            if content.strip().startswith('//'):
                print("Warning: CSV file contains commented lines, which may affect parsing")
            csvfile.seek(0)
            reader = csv.DictReader(csvfile)
            user_count = 0
            for row in reader:
                if 'id' in row and 'password' in row:
                    users.append({"id": row['id'], "password": row['password']})
                    user_count += 1
                else:
                    print(f"Warning: Incorrect user data format: {row}")
            print(f"Successfully loaded {user_count} users")
    except Exception as e:
        print(f"Failed to read user file: {e}")
        users = [{"id": "your_id", "password": "your_password"}]
    return users

user_agents = load_user_agents()
users = load_users()

checkin_code = input("Please enter iCheckin Code (for all users): ").strip()

for user in users:
    print(f"\n🔁 Trying to login user: {user['id']}")
    current_ua = random.choice(user_agents)
    headers = {
        "User-Agent": current_ua,
        "Origin": "https://izone.sunway.edu.my",
        "Referer": LOGIN_URL,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    print(f"📱 Using UA: {current_ua[:30]}...")
    session = requests.Session()
    session.headers.update(headers)
    resp = session.get(LOGIN_URL, verify=False)
    soup = BeautifulSoup(resp.text, 'html.parser')
    nc_token = soup.find("input", {"name": "__ncforminfo"})
    nc_value = nc_token["value"] if nc_token else ""
    login_data = {
        "form_action": "submitted",
        "student_uid": user["id"],
        "password": user["password"],
        "g-recaptcha-response": "",
        "__ncforminfo": nc_value
    }
    resp_post = session.post(LOGIN_URL, data=login_data, verify=False)
    soup2 = BeautifulSoup(resp_post.text, 'html.parser')
    error_msg = soup2.find(id="msg")
    if error_msg:
        if "invalid" in error_msg.text.lower():
            print(f"❌ User {user['id']} login failed:", error_msg.text.strip())
            print(f"ℹ️ Tip: Please check if ID and password are correct, 'xxxxxxxxxx' is not a valid password")
            continue
        else:
            print(f"⚠️ User {user['id']} login warning:", error_msg.text.strip())
    if "logout" not in resp_post.text.lower():
        print(f"❌ User {user['id']} may have failed to login: login page element not detected")
        continue
    resp_profile = session.get(PROFILE_URL, verify=False)
    soup_profile = BeautifulSoup(resp_profile.text, 'html.parser')
    name_tag = soup_profile.find("div", class_="panel-heading")
    username = name_tag.text.strip() if name_tag else f"{user['id']}"
    checkin_payload = {"checkin_code": checkin_code}
    resp_checkin = session.post(CHECKIN_URL, data=checkin_payload, verify=False)
    soup_checkin = BeautifulSoup(resp_checkin.text, "html.parser")
    alerts = soup_checkin.find_all("div", class_="alert")
    found = False
    for alert in alerts:
        text = alert.get_text(strip=True)
        if "already checked in" in text.lower() or "have already checked in" in text.lower():
            print(f"⚠️ User {username} has already checked in:", text)
            found = True
            break
        elif "not valid" in text.lower() or "not in this class" in text.lower():
            print(f"❌ User {username} check-in failed:", text)
            found = True
            break
    if not found:
        print(f"✅ User {username} checked in successfully!")
