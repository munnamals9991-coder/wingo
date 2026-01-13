import requests
import time
import threading
import telebot

# --- কনফিগারেশন ---
BOT_TOKEN = "8549383809:AAGag6sExLJFPG3BrEj1xfMK8Mn-VaCmFEs"
CHAT_ID = "-1003466119460"
FB_BASE_URL = "https://hidndnd-default-rtdb.firebaseio.com/live"
AUTH_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJUb2tlblR5cGUiOiJBY2Nlc3NfVG9rZW4iLCJUZW5hbnRJZCI6IjEwODEiLCJVc2VySWQiOiIxMDgxMDAwMDYyODczOCIsIkFnZW50Q29kZSI6IjEwODEwMSIsIlRlbmFudEFjY291bnQiOiI2Mjg3MzgiLCJMb2dpbklQIjoiMTU3LjE1LjEyMS4xMDAiLCJMb2dpblRpbWUiOiIxNzY4MjIxNjQ0ODE1IiwiU3lzQ3VycmVuY3kiOiJCRFQiLCJTeXNMYW5ndWFnZSI6ImVuIiwiRGV2aWNlVHlwZSI6IkFuZHJvaWQiLCJMb3R0ZXJ5TGltaXRHcm91cE51bSI6IjAiLCJVc2VyVHlwZSI6IjAiLCJuYmYiOjE3NjgyMjE2OTIsImV4cCI6MTc2ODIyNTI5MiwiaXNzIjoiand0SXNzdWVyIiwiYXVkIjoibG90dGVyeVRpY2tldCJ9.5EOhWweWgKaOY3NKIvlKFG89HfmVyIkrK-dLnjEtrVc"

bot = telebot.TeleBot(BOT_TOKEN)
dice_map = {"1":"⚀","2":"⚁","3":"⚂","4":"⚃","5":"⚄","6":"⚅"}

def sync_to_firebase(path, data):
    try:
        requests.put(f"{FB_BASE_URL}/{path}.json", json=data, timeout=5)
    except: pass

# --- ১. WinGo 30S লজিক ---
def wingo_task():
    last_issue = None
    url = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"
    print("🟢 WinGo Task Started")
    while True:
        try:
            r = requests.get(url, headers={'Authorization': AUTH_TOKEN}, params={'ts': int(time.time()*1000)}, timeout=10)
            data = r.json()['data']['list'][0]
            issue = data.get('issueNumber') or data.get('issue')
            if issue != last_issue:
                val = int(data.get('number'))
                size = "BIG 🟢" if val >= 5 else "SMALL 🔴"
                sync_to_firebase("wingo", {"period": issue, "result": str(val), "analysis": size})
                msg = f"💎 **WINGO 30S RESULT** 💎\n━━━━━━━━━━━━━━━━━━━━\n🆔 **Period:** `{issue}`\n🔢 **Number:** `{val}`\n📏 **Size:** `{size}`\n━━━━━━━━━━━━━━━━━━━━\n⚡ **Powered By Zone**"
                bot.send_message(CHAT_ID, msg, parse_mode='Markdown')
                last_issue = issue
        except: pass
        time.sleep(2)

# --- ২. 5D 1M লজিক ---
def d5_task():
    last_issue = None
    url = "https://draw.ar-lottery01.com/D5/D5_1M/GetHistoryIssuePage.json"
    print("🔵 5D Task Started")
    while True:
        try:
            r = requests.get(url, headers={'Authorization': AUTH_TOKEN}, params={'ts': int(time.time()*1000)}, timeout=10)
            data = r.json()['data']['list'][0]
            issue = data.get('issueNumber') or data.get('issue')
            if issue != last_issue:
                res = str(data.get('premium'))
                total = data.get('sum', '0')
                sync_to_firebase("d5", {"period": issue, "result": res, "sum": total})
                msg = f"🏆 **5D 1M RESULT** 🏆\n━━━━━━━━━━━━━━━━━━━━\n📅 **Period:** `{issue}`\n🔢 **Result:** [ `{' '.join(list(res))}` ]\n📊 **Total Sum:** `{total}`\n━━━━━━━━━━━━━━━━━━━━\n⚡ **Powered By Zone**"
                bot.send_message(CHAT_ID, msg, parse_mode='Markdown')
                last_issue = issue
        except: pass
        time.sleep(2)

# --- ৩. K3 1M লজিক ---
def k3_task():
    last_issue = None
    url = "https://draw.ar-lottery01.com/K3/K3_1M/GetHistoryIssuePage.json"
    print("🔴 K3 Task Started")
    while True:
        try:
            r = requests.get(url, headers={'Authorization': AUTH_TOKEN}, params={'ts': int(time.time()*1000)}, timeout=10)
            data = r.json()['data']['list'][0]
            issue = data.get('issueNumber') or data.get('issue')
            if issue != last_issue:
                res_raw = str(data.get('number')).replace(",","")
                total = data.get('sum', '0')
                dices = " ".join([dice_map.get(d, d) for d in res_raw])
                sync_to_firebase("k3", {"period": issue, "result": res_raw, "sum": total})
                msg = f"🎲 **K3 1M RESULT** 🎲\n━━━━━━━━━━━━━━━━━━━━\n📅 **Period:** `{issue}`\n🎰 **Dices:** {dices}\n📊 **Sum:** `{total}` | `{'BIG 🟢' if int(total)>=11 else 'SMALL 🔴'}`\n━━━━━━━━━━━━━━━━━━━━\n⚡ **Powered By Zone**"
                bot.send_message(CHAT_ID, msg, parse_mode='Markdown')
                last_issue = issue
        except: pass
        time.sleep(2)

# --- সবগুলো একসাথে চালানো ---
if __name__ == "__main__":
    threading.Thread(target=wingo_task).start()
    threading.Thread(target=d5_task).start()
    threading.Thread(target=k3_task).start()
