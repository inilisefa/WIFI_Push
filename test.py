import json
import os
import time
import schedule
import requests


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
    expiretime = data["expiretime"]  # 2025-08-03

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


def send_dingtalk_msg(data: dict):
    dev_no = data.get('dev_no')
    totalAmount = data.get('totalAmount')
    remainAmount = data.get('remainAmount')
    expiretime = data.get('expiretime')
    devicePower = data.get('devicePower')
    runningTime = data.get('runningTime')
    hotspotName = data.get('hotspotName')
    today_usage = data.get('today_usage')
    access_token = os.environ.get('DINGTALK_ACCESS_TOKEN')
    url = f'https://oapi.dingtalk.com/robot/send?access_token={access_token}'
    playload = {
        "msgtype": "markdown",
        "markdown": {
            "title": "随身WiFi使用情况",
            "text": f"# 随身WiFi使用情况 \n\n"
                    f"#### 设备号: {dev_no}\n"
                    f"#### 总流量: {totalAmount} GB\n"
                    f"#### 剩余流量: {remainAmount} GB\n"
                    f"#### 今日已用: {today_usage} GB\n"
                    f"#### 设备电量: {devicePower}%\n"
                    f"#### 设备已运行: {runningTime}\n"
                    f"#### 热点名称: {hotspotName}\n"
                    f"#### 到期时间: {expiretime}\n\n"
                    f"> ###### 数据更新时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
        },
        "at": {
            "atUserIds": [
                "manager1573"
            ],
            "isAtAll": True
        }
    }
    response = requests.post(url, json=playload)
    print(response.json())


def job():
    """
    定时任务函数，获取WiFi信息并发送钉钉消息
    """
    try:
        print(f"执行定时任务: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
        res = get_portable_wifi_info()
        send_dingtalk_msg(res)
        print("定时任务执行完成")
    except Exception as e:
        print(f"定时任务执行出错: {e}")


if __name__ == '__main__':
    schedule.every().hour.do(job)
    job()
    while True:
        schedule.run_pending()
        time.sleep(60)
