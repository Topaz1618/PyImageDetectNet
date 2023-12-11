"""
Author: Hang Yan
Date created: 2023/10/7
Email: topaz1668@gmail.com

This code is licensed under the GNU General Public License v3.0.
"""
import os
import requests


def set_proxy(proxy_address, http_port, https_port):
    """
    Set HTTP and HTTPS proxies.
    """
    http_proxy = f"http://{proxy_address}:{http_port}"
    https_proxy = f"http://{proxy_address}:{https_port}"

    os.environ['http_proxy'] = http_proxy
    os.environ['https_proxy'] = https_proxy

    proxies = {
        'http': http_proxy,
        'https': https_proxy
    }
    return proxies

def get_current_ip():
    """
    Get the current IP address.
    """
    response = requests.get('http://ip-api.com/json')
    data = response.json()

    # 提取地理位置信息
    if data['status'] == 'success':
        ip_address = data['query']
        country = data['country']
        region = data['regionName']
        city = data['city']
        print(f"IP地址: {ip_address}")
        print(f"所在地: {city}, {region}, {country}")


def main():
    # Set the proxy
    proxy_address = '127.0.0.1'
    http_port = '9090'
    https_port = '9091'
    set_proxy(proxy_address, http_port, https_port)

    # Get the current IP address
    get_current_ip()


if __name__ == '__main__':
    main()