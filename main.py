import os
import time
import requests
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage

# APP_ID = os.getenv('APP_ID')
# APP_SECRET = os.getenv('APP_SECRET')
# TEMPALTE_ID = os.getenv('TEMPALTE_ID')
# OPEN_ID = os.getenv('OPEN_ID')
APP_ID = 'wxb6641a5b9842360c'
APP_SECRET = '076088b325d3243a3365cf440bdc5196'
TEMPALTE_ID = '8Rnfw5hk-gl-s6qVhvfd9YTg-a6KSsbwojLVY6Ccm74'
OPEN_ID = 'o7YypvrA4d8mYGlLsvTEoHNaESMQ'


def get_access_token() -> str:
    appid = APP_ID
    secret = APP_SECRET
    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}'
    res = requests.get(url).json()
    return res['access_token']


def send_template_msg(OPEN_ID: str, data: dict, url: str):
    totalAmount = data.get('totalAmount')
    remainAmount = data.get('remainAmount')
    expiretime = data.get('expiretime')
    devicePower = data.get('devicePower')
    runningTime = data.get('runningTime')
    hotspotName = data.get('hotspotName')
    today_usage = data.get('today_usage')
    access_token = get_access_token()
    data = {
        "touser": OPEN_ID,
        "template_id": TEMPALTE_ID,  # 在公众号后台新建模板后获得
        "url": url,
        "data": {
            "totalAmount": {"value": totalAmount, "color": "#FF0000"},  # 绿色
            "remainAmount": {"value": remainAmount, "color": "#6FB98F"},  # 绿色
            "expiretime": {"value": expiretime, "color": "#6FB98F"},  # 绿色
            "devicePower": {"value": devicePower, "color": "#6FB98F"},  # 绿色
            "runningTime": {"value": runningTime, "color": "#6FB98F"},  # 绿色
            "hotspotName": {"value": hotspotName, "color": "#6FB98F"},  # 绿色
            "today_usage": {"value": today_usage, "color": "#6FB98F"},  # 绿色
        }
    }
    url = f'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}'
    res = requests.post(url, json=data)
    print(res.text)


def get_portable_wifi_info() -> dict:
    url = 'http://wifi.ruijiadashop.cn/api/Card/loginCard'
    params = {
        'dev_no': '8182350068',
        'type': 2,
    }
    response = requests.post(url, json=params)
    data = response.json()
    data = data["data"]

    # 流量相关
    totalAmount = f'{float(data["totalAmount"]) / 1024:.2f}'
    remainAmount = f"{float(data["remainAmount"]) / 1024:.2f}"
    equipment = data["equipment"]
    expiretime = equipment["reportTime"]  # 2025-08-03

    # 设备相关
    devicePower = equipment["devicePower"]
    runningTime = equipment["runningTime"]
    hotspotName = equipment["hotspotName"]
    dev_no = equipment["dev_no"]
    useage = float(totalAmount) - float(remainAmount)
    res = {
        "dev_no": dev_no,
        "totalAmount": totalAmount,
        "remainAmount": remainAmount,
        "expiretime": expiretime,
        "devicePower": devicePower,
        "runningTime": runningTime,
        "hotspotName": hotspotName,
        'today_usage': f'{useage:.2f}'
    }
    return res


if __name__ == '__main__':
    while True:
        send_template_msg(
            OPEN_ID=OPEN_ID,
            data=get_portable_wifi_info(),
            url='http://wifi.ruijiadashop.cn/index.html#/'
        )
        time.sleep(60)
    res = get_portable_wifi_info()
    print(res)
