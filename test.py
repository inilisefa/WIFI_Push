import socket


def ip_to_domain(ip_address):
    """
    通过IP地址查询对应的域名
    :param ip_address: 要查询的IP地址
    :return: 域名或错误信息
    """
    try:
        # 验证IP地址格式
        socket.inet_aton(ip_address)

        # 进行反向DNS查询
        host_info = socket.gethostbyaddr(ip_address)

        # 返回主机名（域名）
        return f"查询成功：\nIP: {ip_address}\n域名: {host_info[0]}"

    except socket.error as e:
        if "not found" in str(e).lower():
            return f"查询失败：IP {ip_address} 没有对应的反向解析记录"
        elif "invalid argument" in str(e).lower():
            return f"错误：无效的IP地址格式 - {ip_address}"
        else:
            return f"查询出错：{str(e)}"
    except Exception as e:
        return f"发生未知错误：{str(e)}"


if __name__ == "__main__":
    # 示例IP：8.8.8.8（Google DNS服务器）
    ip = input("请输入要查询的IP地址：")
    result = ip_to_domain(ip)
    print(result)
