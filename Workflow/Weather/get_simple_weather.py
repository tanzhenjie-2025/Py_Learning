import requests
import sys


def get_simple_weather(city, date):
    """极简版天气查询"""
    try:
        # 使用wttr.in的简化API
        url = f"http://wttr.in/{city}?format=%C+%t+%h+%w&lang=zh"
        response = requests.get(url)

        if response.status_code == 200:
            weather_info = response.text.strip()
            return f"{date} {city}的天气: {weather_info}"
        else:
            return "获取天气信息失败"

    except Exception as e:
        return f"错误: {str(e)}"


# 测试
if __name__ == "__main__":
    city = '茂名'
    date = '2025-11-10'

    result = get_simple_weather(city, date)
    print(result)