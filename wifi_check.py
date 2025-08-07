import json
import os
import time
import requests
import logging
from typing import Dict, Any

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('wifi_monitor.log'),
        logging.StreamHandler()
    ]
)

# 常量定义
WIFI_API_URL = 'http://dongle.ruijiadashop.cn/api/Card/loginCard'
DINGTALK_WEBHOOK = 'https://oapi.dingtalk.com/robot/send'
# DINGTALK_ACCESS_TOKEN = os.getenv('DINGTALK_ACCESS_TOKEN')
DINGTALK_ACCESS_TOKEN = os.getenv('DINGTALK_ACCESS_TOKEN')
DEVICE_NO = '8182350068'
AT_USER_IDS = ["manager1573"]


def get_portable_wifi_info() -> Dict[str, Any]:
    """
    获取便携WiFi设备信息
    :return: 包含设备信息的字典
    """
    try:
        params = {
            'dev_no': DEVICE_NO,
            'type': 2,
        }
        response = requests.post(WIFI_API_URL, json=params, timeout=10)
        response.raise_for_status()  # 检查HTTP请求是否成功
        data = response.json().get("data", {})

        # 流量相关
        total_amount = float(data.get('totalAmount', 0)) / 1024
        remain_amount = float(data.get('remainAmount', 0)) / 1024
        equipment = data.get("equipment", {})

        # 设备相关
        usage = total_amount - remain_amount
        return {
            "dev_no": equipment.get("dev_no", ""),
            "totalAmount": f"{total_amount:.2f}",
            "remainAmount": f"{remain_amount:.2f}",
            "expiretime": data.get("expiretime", ""),
            "devicePower": equipment.get("devicePower", ""),
            "runningTime": equipment.get("runningTime", ""),
            "hotspotName": equipment.get("hotspotName", ""),
            'today_usage': f'{usage:.2f}'
        }
    except requests.exceptions.RequestException as e:
        logging.error(f"获取WiFi信息失败: {e}")
        raise
    except Exception as e:
        logging.error(f"处理WiFi信息时发生错误: {e}")
        raise


def send_dingtalk_msg(data: Dict[str, Any]) -> bool:
    """
    发送钉钉机器人消息
    :param data: 包含设备信息的字典
    :return: 是否发送成功
    """
    try:
        url = f'{DINGTALK_WEBHOOK}?access_token={DINGTALK_ACCESS_TOKEN}'
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": "随身WiFi使用情况",
                "text": (
                    f"# 随身WiFi使用情况 \n\n"
                    f"#### 设备号: {data.get('dev_no', '')}\n"
                    f"#### 总流量: {data.get('totalAmount', '')} GB\n"
                    f"#### 剩余流量: {data.get('remainAmount', '')} GB\n"
                    f"#### 今日已用: {data.get('today_usage', '')} GB\n"
                    f"#### 设备电量: {data.get('devicePower', '')}%\n"
                    f"#### 设备已运行: {data.get('runningTime', '')}\n"
                    f"#### 热点名称: {data.get('hotspotName', '')}\n"
                    f"#### 到期时间: {data.get('expiretime', '')}\n\n"
                    f"> ###### 数据更新时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
                )
            },
            "at": {
                "atUserIds": AT_USER_IDS,
                "isAtAll": True  # 根据需求调整是否@所有人
            }
        }
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        logging.info("钉钉消息发送成功")
        return True
    except requests.exceptions.RequestException as e:
        logging.error(f"发送钉钉消息失败: {e}")
        return False
    except Exception as e:
        logging.error(f"处理钉钉消息时发生错误: {e}")
        return False


def job():
    """
    定时任务函数，获取WiFi信息并发送钉钉消息
    """
    try:
        logging.info(f"开始执行定时任务: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
        wifi_info = get_portable_wifi_info()
        if wifi_info:
            send_dingtalk_msg(wifi_info)
        logging.info("定时任务执行完成")
    except Exception as e:
        logging.error(f"定时任务执行出错: {e}")


if __name__ == '__main__':
    # 单次执行
    get_portable_wifi_info()

    # 如果要设置为定时任务，可以使用以下代码
    # import schedule
    #
    # # 设置每30分钟执行一次
    # schedule.every(30).minutes.do(job)
    #
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)