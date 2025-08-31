from typing import Dict

import requests


def check_wifi_domains_availability():
    """
    检测从wifi1到wifi10的域名可用性
    :return: 包含域名及其可用状态的字典
    """
    for i in range(1, 11):
        try:

            url = f'http://wifi{i}.ruijiadashop.cn/api/Card/loginCard'
            params = {'dev_no': '8182350068', 'type': 2}
            response = requests.post(url, json=params, timeout=10)
            response.raise_for_status()
            data = response.json().get("data", {})
            if data.get('code') == 1:
                return url
        except requests.exceptions.RequestException as e:
            print(f"Error occurred while checking {url}: {e}")
        except Exception as e:
            print(f"Error occurred while checking {url}: {e}")


if __name__ == '__main__':
    url = check_wifi_domains_availability()
    print(url)
