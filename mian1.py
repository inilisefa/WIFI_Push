import requests

base_url = 'https://ssc.9tinfo.com.cn'


def get_device_info():
    try:
        url = f'{base_url}/h5-portal/dmp/realDmpInfo'
        response = requests.post(url, json={"deviceId": "2614743106142076936"})
        data = response.json().get('data').get('realDmpInfo')
        # 电池电量
        battery = data.get('battery')
        # wifi名称
        hotspotName = data.get('hotspotName')
        # 最后一次上线时间
        lastOnlineTime = data.get('lastOnlineTime')
        # 设备是否在线
        onlineStatus = data.get('onlineStatus')
        # 设备序列号
        deviceSn = data.get('deviceSn')
        return {
            'battery': battery,
            'hotspotName': hotspotName,
            'lastOnlineTime': lastOnlineTime,
            'onlineStatus': onlineStatus,
            'deviceSn': deviceSn
        }
    except Exception as e:
        print(e)


def get_internet_data_usage():
    try:
        url = f'{base_url}/h5-portal/device/findDeviceDetail'
        response = requests.post(url, json={"deviceId": "2614743106142076936"})
        data = response.json()
        status = data.get('success')
        if status:
            data = data.get('data')
            print(data)
        else:
            return None

    except Exception as e:
        print(e)


if __name__ == '__main__':
    res = get_device_info()
    get_internet_data_usage()
    print(res)
