import requests
from bs4 import BeautifulSoup

# 创建会话对象
session = requests.Session()

# 设置cookie
cookie = {
    "ipb_member_id": "填入你的ipb_member_id",
    "ipb_pass_hash": "填入你的ipb_pass_hash",
    "igneous": "填入你的igneous"
}
session.cookies.update(cookie)

# 设置 User-Agent 头部信息
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

# 获取新闻页面
news_url = "https://e-hentai.org/news.php"

# 刷新5次新闻页面并打印成功刷新次数
refresh_count = 0
for i in range(5):
    response = session.get(news_url, headers=headers)
    if response.status_code == 200:
        if "receive these site status updates if the site is ever unavailable" in response.text:
            print(f"成功刷新并访问网页 {i+1} 次")
            refresh_count += 1
        else:
            print(f"网页内容不正确 {i+1} 次: {response.status_code} {response.reason}")
    else:
        print(f"刷新网页失败 {i+1} 次: {response.status_code} {response.reason}")
    
if refresh_count == 0:
    print("未能成功访问目标网页")
else:
    print(f"成功刷新总数: {refresh_count}")

# 访问 Hath 交易页面并解析 HTML
exchange_url = "https://e-hentai.org/exchange.php?t=hath"
response = session.get(exchange_url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# 获取并打印剩余Credits和Hath
credits = soup.find_all("div", {"style": "margin-top:5px; font-weight:bold"})[0].text.split(":")[1].strip()
hath = soup.find_all("div", {"style": "margin-top:5px; font-weight:bold"})[1].text.split(":")[1].strip()

# 访问 GP 交易页面并解析 HTML
exchange_url = "https://e-hentai.org/exchange.php?t=gp"
response = session.get(exchange_url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# 获取并打印剩余GP
kGP = soup.find_all("div", {"style": "margin-top:5px; font-weight:bold"})[1].text.split(":")[1].strip()
print("剩余Credits：" + credits + "  剩余Hath：" + hath + "  剩余GP：" + kGP)

# Telegram Bot的访问令牌
TOKEN = '填入你的机器人TOKEN'
# Telegram 推送目标的聊天ID，可以是单个用户的ID或者群组的ID
CHAT_ID = '填入你的CHAT_ID'

def send_telegram_message(message):
    """使用Telegram Bot发送一条消息"""
    # Telegram Bot API的基本URL
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    # 消息的参数
    params = {'chat_id': CHAT_ID, 'text': message.replace("  ", "n")}
    # 发送POST请求
    response = requests.post(url, data=params)
    # 如果发送失败，打印错误信息
    if response.status_code != 200:
        print(f"Error sending message: {response.status_code} - {response.text}")
    else:
        print("消息推送成功")

# 调用函数发送一条消息
send_telegram_message(f"UID: {session.cookies['ipb_member_id']} 成功领取E-Hentai每日奖励\n剩余Credits：{credits}\n剩余Hath：{hath}\n剩余GP：{kGP}")

# 退出会话
session.close()