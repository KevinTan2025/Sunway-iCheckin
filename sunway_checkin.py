import requests
from bs4 import BeautifulSoup
import csv
import json
import random
import os
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LOGIN_URL = "https://izone.sunway.edu.my/login"
CHECKIN_URL = "https://izone.sunway.edu.my/icheckin/iCheckinNowWithCode"
PROFILE_URL = "https://izone.sunway.edu.my/student/myProfile"

# When packaged with PyInstaller (sys.frozen), __file__ points inside a
# temporary extraction directory that is removed after execution. To persist
# user files next to the executable, resolve paths differently in that case.
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

USERS_JSON = os.path.join(BASE_DIR, "users.json")
USERS_CSV = os.path.join(BASE_DIR, "users.csv")

# Built-in list of User-Agent strings. `ua.csv` can override or extend this
# list if present in the same directory as the script or packaged executable.
DEFAULT_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/136.0.0.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
]

def load_user_agents():
    """Return a list of User-Agent strings."""
    ua_file = os.path.join(BASE_DIR, "ua.csv")
    user_agents = []
    if os.path.exists(ua_file):
        try:
            with open(ua_file, "r", encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)
                for row in reader:
                    if row and row[0].strip():
                        user_agents.append(row[0].strip())
        except Exception as e:
            print(f"Failed to read user agent file: {e}")

    if not user_agents:
        user_agents = DEFAULT_USER_AGENTS
    return user_agents

def load_users():
    """Load users from a JSON file if it exists, otherwise fall back to CSV."""
    users = []
    if os.path.exists(USERS_JSON):
        try:
            with open(USERS_JSON, "r", encoding="utf-8") as f:
                users = json.load(f)
        except Exception as e:
            print(f"Failed to read {USERS_JSON}: {e}")
    else:
        try:
            with open(USERS_CSV, "r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if "id" in row and "password" in row:
                        users.append({"id": row["id"], "password": row["password"], "memo": row.get("memo", "")})
        except Exception as e:
            print(f"Failed to read {USERS_CSV}: {e}")
    return users


def save_users(users):
    """Save user list to JSON."""
    try:
        with open(USERS_JSON, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2)
    except Exception as e:
        print(f"Failed to save {USERS_JSON}: {e}")

def checkin_user(user, checkin_code, user_agents, log=print):
    log(f"\n🔁 Trying to login user: {user['id']}")
    current_ua = random.choice(user_agents)
    headers = {
        "User-Agent": current_ua,
        "Origin": "https://izone.sunway.edu.my",
        "Referer": LOGIN_URL,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    log(f"📱 Using UA: {current_ua[:30]}...")
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
        "__ncforminfo": nc_value,
    }
    resp_post = session.post(LOGIN_URL, data=login_data, verify=False)
    soup2 = BeautifulSoup(resp_post.text, 'html.parser')
    error_msg = soup2.find(id="msg")
    if error_msg:
        if "invalid" in error_msg.text.lower():
            log(f"❌ User {user['id']} login failed: {error_msg.text.strip()}")
            return False
        else:
            log(f"⚠️ User {user['id']} login warning: {error_msg.text.strip()}")
    if "logout" not in resp_post.text.lower():
        log(f"❌ User {user['id']} may have failed to login: login page element not detected")
        return False

    resp_profile = session.get(PROFILE_URL, verify=False)
    soup_profile = BeautifulSoup(resp_profile.text, 'html.parser')
    name_tag = soup_profile.find("div", class_="panel-heading")
    username = name_tag.text.strip() if name_tag else f"{user['id']}"

    checkin_payload = {"checkin_code": checkin_code}
    resp_checkin = session.post(CHECKIN_URL, data=checkin_payload, verify=False)
    soup_checkin = BeautifulSoup(resp_checkin.text, "html.parser")
    alerts = soup_checkin.find_all("div", class_="alert")
    for alert in alerts:
        text = alert.get_text(strip=True)
        if "already checked in" in text.lower() or "have already checked in" in text.lower():
            log(f"⚠️ User {username} has already checked in: {text}")
            return True
        elif "not valid" in text.lower() or "not in this class" in text.lower():
            log(f"❌ User {username} check-in failed: {text}")
            return False
    log(f"✅ User {username} checked in successfully!")
    return True
