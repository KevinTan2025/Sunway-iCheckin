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

# 从CSV文件读取用户代理
def load_user_agents():
    user_agents = []
    ua_file = os.path.join(os.path.dirname(__file__), 'ua.csv')
    try:
        with open(ua_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # 跳过表头
            for row in reader:
                if row and row[0].strip():
                    user_agents.append(row[0].strip())
    except Exception as e:
        print(f"无法读取用户代理文件: {e}")
        # 如果无法读取文件，提供默认UA
        user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"]
    return user_agents

# 从CSV文件读取用户信息
def load_users():
    users = []
    users_file = os.path.join(os.path.dirname(__file__), 'users.csv')
    try:
        print(f"正在读取用户文件: {users_file}")
        with open(users_file, 'r') as csvfile:
            # 跳过可能存在的注释行
            content = csvfile.read()
            if content.strip().startswith('//'):
                print("警告: CSV文件包含注释行，可能影响解析")
            
            # 重新打开文件进行解析
            csvfile.seek(0)
            reader = csv.DictReader(csvfile)
            user_count = 0
            for row in reader:
                if 'id' in row and 'password' in row:
                    users.append({"id": row['id'], "password": row['password']})
                    user_count += 1
                else:
                    print(f"警告: 用户数据格式不正确: {row}")
            print(f"成功读取 {user_count} 个用户")
    except Exception as e:
        print(f"无法读取用户文件: {e}")
        # 如果无法读取文件，提供示例用户
        users = [{"id": "24018566", "password": "xxxxxxxxxx"}]
    return users

# 读取用户代理和用户信息
user_agents = load_user_agents()
users = load_users()

# 📥 获取打卡码（一次输入，供所有人共用）
checkin_code = input("请输入 iCheckin Code（供所有人打卡）: ").strip()

# ▶ 每个用户循环登录打卡
for user in users:
    print(f"\n🔁 尝试登录用户：{user['id']}")
    
    # 为每个用户随机选择一个UA
    current_ua = random.choice(user_agents)
    
    # 设置当前用户的请求头
    headers = {
        "User-Agent": current_ua,
        "Origin": "https://izone.sunway.edu.my",
        "Referer": LOGIN_URL,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    print(f"📱 使用UA: {current_ua[:30]}...")
    
    session = requests.Session()
    session.headers.update(headers)

    # 获取 __ncforminfo
    resp = session.get(LOGIN_URL, verify=False)
    soup = BeautifulSoup(resp.text, 'html.parser')
    nc_token = soup.find("input", {"name": "__ncforminfo"})
    nc_value = nc_token["value"] if nc_token else ""

    # 登录数据
    login_data = {
        "form_action": "submitted",
        "student_uid": user["id"],
        "password": user["password"],
        "g-recaptcha-response": "",
        "__ncforminfo": nc_value
    }

    # 登录请求
    resp_post = session.post(LOGIN_URL, data=login_data, verify=False)
    soup2 = BeautifulSoup(resp_post.text, 'html.parser')
    error_msg = soup2.find(id="msg")

    # 详细检查登录状态
    if error_msg:
        if "invalid" in error_msg.text.lower():
            print(f"❌ 用户 {user['id']} 登录失败：", error_msg.text.strip())
            print(f"   ℹ️ 提示: 请检查ID和密码是否正确，'xxxxxxxxxx'不是有效密码")
            continue
        else:
            print(f"⚠️ 用户 {user['id']} 登录警告：", error_msg.text.strip())
    
    # 检查是否实际登录成功
    if "logout" not in resp_post.text.lower():
        print(f"❌ 用户 {user['id']} 可能登录失败：未检测到登录后的页面元素")
        continue

    # 获取用户名
    resp_profile = session.get(PROFILE_URL, verify=False)
    soup_profile = BeautifulSoup(resp_profile.text, 'html.parser')
    name_tag = soup_profile.find("div", class_="panel-heading")
    username = name_tag.text.strip() if name_tag else f"{user['id']}"

    # 提交打卡请求
    checkin_payload = {"checkin_code": checkin_code}
    resp_checkin = session.post(CHECKIN_URL, data=checkin_payload, verify=False)
    soup_checkin = BeautifulSoup(resp_checkin.text, "html.parser")
    alerts = soup_checkin.find_all("div", class_="alert")

    found = False
    for alert in alerts:
        text = alert.get_text(strip=True)
        if "already checked in" in text.lower() or "have already checked in" in text.lower():
            print(f"⚠️ 用户 {username} 已打过卡：", text)
            found = True
            break
        elif "not valid" in text.lower() or "not in this class" in text.lower():
            print(f"❌ 用户 {username} 打卡失败：", text)
            found = True
            break

    if not found:
        print(f"✅ 用户 {username} 打卡成功！")
