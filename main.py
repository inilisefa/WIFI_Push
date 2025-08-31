import os
import time
import requests
import logging
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage
from wechatpy.exceptions import WeChatClientException

from utils import check_wifi_domains_availability

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
OPEN_ID = os.getenv('OPEN_ID')
# TEMPLATE_ID = os.getenv('TEMPLATE_ID','y0Ln9bKBclhw6L8QqX_ygAs-3Jr78OfIHSu_kgaZvIU')
TEMPLATE_ID = 'y0Ln9bKBclhw6L8QqX_ygAs-3Jr78OfIHSu_kgaZvIU'


class WeChatMonitor:
    def __init__(self):
        self.client = WeChatClient(
            os.getenv('APP_ID'),
            os.getenv('APP_SECRET')
        )
        self.message_api = WeChatMessage(self.client)

    def get_wifi_info(self) -> dict:
        """获取WiFi设备信息"""
        try:
            url = check_wifi_domains_availability()
            params = {'dev_no': '8182350068', 'type': 2}
            response = requests.post(url, json=params, timeout=10)
            response.raise_for_status()
            data = response.json().get("data", {})

            equipment = data.get("equipment", {})
            total = float(data.get("totalAmount", 0)) / 1024
            remain = float(data.get("remainAmount", 0)) / 1024

            return {
                "dev_no": equipment.get("dev_no", "N/A"),
                "totalAmount": f"{total:.2f}",
                "remainAmount": f"{remain:.2f}",
                "expiretime": data.get("expiretime", "N/A"),
                "devicePower": equipment.get("devicePower", "N/A"),
                "runningTime": equipment.get("runningTime", "N/A"),
                "hotspotName": equipment.get("hotspotName", "N/A"),
                "today_usage": f"{total - remain:.2f}"
            }

        except Exception as e:
            logging.error(f"获取WiFi信息失败: {e}")
            raise

    def send_alert(self, data: dict):
        """发送微信模板消息"""
        try:
            template_data = {
                "dev_no": {"value": data['dev_no'], "color": "#FF0000"},
                "totalAmount": {"value": data['totalAmount'], "color": "#FF0000"},
                "remainAmount": {"value": data['remainAmount'], "color": "#6FB98F"},
                "expiretime": {"value": data['expiretime'], "color": "#6FB98F"},
                "devicePower": {"value": data['devicePower'], "color": "#6FB98F"},
                "runningTime": {"value": data['runningTime'], "color": "#6FB98F"},
                "hotspotName": {"value": data['hotspotName'], "color": "#6FB98F"},
                "today_usage": {"value": data['today_usage'], "color": "#6FB98F"}
            }

            self.message_api.send_template(
                OPEN_ID,
                TEMPLATE_ID,
                template_data,
                url='https://wifi.ruijiadashop.cn/index.html'
            )
            logging.info("微信消息发送成功")

        except WeChatClientException as e:
            logging.error(f"微信接口错误: {e}")
        except Exception as e:
            logging.error(f"消息发送异常: {e}")


if __name__ == '__main__':
    monitor = WeChatMonitor()
    try:
        wifi_data = monitor.get_wifi_info()
        monitor.send_alert(wifi_data)
    except KeyboardInterrupt:
        logging.info("程序手动终止")
    except Exception as e:
        logging.error(f"主循环异常: {e}")
