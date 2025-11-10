import requests
import sys
from datetime import datetime, timedelta


def translate_weather_to_chinese(weather_desc):
    """将英文天气描述翻译为中文"""
    weather_mapping = {
        'clear': '晴天',
        'sunny': '晴朗',
        'cloud': '多云',
        'overcast': '阴天',
        'rain': '降雨',
        'light rain': '小雨',
        'moderate rain': '中雨',
        'heavy rain': '大雨',
        'shower': '阵雨',
        'thunderstorm': '雷雨',
        'snow': '降雪',
        'light snow': '小雪',
        'heavy snow': '大雪',
        'fog': '雾',
        'mist': '薄雾',
        'haze': '雾霾',
        'drizzle': '毛毛雨',
        'partly cloudy': '局部多云',
        'scattered clouds': '零星云',
        'broken clouds': '多云间晴',
        'few clouds': '少云'
    }

    # 将描述转为小写进行匹配
    desc_lower = weather_desc.lower()

    # 查找匹配的中文描述
    for eng, chs in weather_mapping.items():
        if eng in desc_lower:
            return chs

    # 如果没有匹配，返回原始描述
    return weather_desc


def get_hour_name(hour):
    """根据小时数获取中文时间名称"""
    return f"{hour}时"  # 优化显示为"X时"


def get_weather_wttr(city_name, target_date):
    """
    使用wttr.in获取指定日期的天气预报
    返回该天每个时间点的具体数据
    """
    try:
        url = f"http://wttr.in/{city_name}?format=j1"
        response = requests.get(url)
        if response.status_code != 200:
            return {"error": "获取天气信息失败（服务器响应异常）"}

        data = response.json()

        # 查找目标日期的天气数据
        weather_day = None
        for day in data['weather']:
            if day['date'] == target_date:
                weather_day = day
                break

        if not weather_day:
            return {"error": f"找不到 {target_date} 的天气预报"}

        # 提取每个小时的天气数据
        hourly_data = []
        for hour_data in weather_day['hourly']:
            try:
                minutes_from_midnight = int(hour_data['time'])
                hour_int = minutes_from_midnight // 100  # 转换为小时数（0-23）

                # 转换天气描述为中文
                chinese_weather = translate_weather_to_chinese(
                    hour_data['weatherDesc'][0]['value']
                )

                hourly_data.append({
                    'hour': hour_int,
                    'hour_name': get_hour_name(hour_int),
                    'temperature': int(hour_data['tempC']),
                    'feels_like': int(hour_data['FeelsLikeC']),
                    'chinese_weather': chinese_weather,
                    'humidity': int(hour_data['humidity']),
                    'wind_speed': int(hour_data['windspeedKmph'])
                })
            except Exception as e:
                print(f"解析小时数据出错: {e}")
                continue

        # 按小时排序
        hourly_data.sort(key=lambda x: x['hour'])

        return {
            'city': data['nearest_area'][0]['areaName'][0]['value'],
            'country': data['nearest_area'][0]['country'][0]['value'],
            'target_date': target_date,
            'hourly_data': hourly_data
        }

    except Exception as e:
        return {"error": f"获取天气信息失败: {str(e)}"}


def format_weather_output(multi_day_weather):
    """格式化多天天气输出"""
    output = []
    # 添加总体标题
    output.append(f"📊 未来{len(multi_day_weather)}天天气预报")
    output.append("=" * 70)

    # 天气图标映射
    weather_icons = {
        '晴天': '☀️', '晴朗': '☀️',
        '多云': '☁️', '局部多云': '⛅', '零星云': '🌤️', '多云间晴': '⛅', '少云': '🌤️',
        '阴天': '☁️',
        '降雨': '🌧️', '小雨': '🌦️', '中雨': '🌧️', '大雨': '💦', '阵雨': '🌦️', '毛毛雨': '🌦️',
        '雷雨': '⛈️',
        '降雪': '❄️', '小雪': '🌨️', '大雪': '❄️',
        '雾': '🌫️', '薄雾': '🌫️', '雾霾': '😷'
    }

    # 遍历每天的天气数据
    for day_idx, weather_data in enumerate(multi_day_weather, 1):
        if 'error' in weather_data:
            output.append(f"\n❌ 第{day_idx}天数据错误: {weather_data['error']}")
            continue

        # 添加日期分隔线
        if day_idx > 1:
            output.append("\n" + "-" * 70)

        # 添加城市和日期信息
        output.append(f"\n🌍 城市: {weather_data['city']}, {weather_data['country']}")
        output.append(f"📅 日期: {weather_data['target_date']}（第{day_idx}天）")
        output.append("⏰ 24小时天气详情：")
        output.append("-" * 70)

        # 添加每小时数据
        for hour_data in weather_data['hourly_data']:
            chinese_weather = hour_data.get('chinese_weather', '未知')
            icon = weather_icons.get(chinese_weather, '🌈')

            output.append(
                f"{icon} {hour_data['hour_name']}: "
                f"{chinese_weather} | "
                f"温度: {hour_data['temperature']}°C | "
                f"体感: {hour_data['feels_like']}°C | "
                f"湿度: {hour_data['humidity']}% | "
                f"风速: {hour_data['wind_speed']}km/h"
            )

    return '\n'.join(output)


def main_wttr(city='茂名', date_input='2025-11-10', prediction=3):
    # 参数验证
    if not city or not date_input:
        print("错误：城市名称和日期都不能为空！")
        return

    if prediction < 1:
        print("错误：预测天数必须至少为1天！")
        return

    try:
        # 解析起始日期
        start_date = datetime.strptime(date_input, "%Y-%m-%d")
    except ValueError:
        print("错误：日期格式不正确，请使用'YYYY-MM-DD'格式（例如：2025-11-10）")
        return

    # 生成需要预测的所有日期
    target_dates = []
    for i in range(prediction):
        current_date = start_date + timedelta(days=i)
        target_dates.append(current_date.strftime("%Y-%m-%d"))

    print(f"\n正在查询 {city} 从 {target_dates[0]} 开始的 {prediction} 天天气预报...")
    print("=" * 70)

    # 获取每天的天气数据
    all_weather = []
    for date in target_dates:
        all_weather.append(get_weather_wttr(city, date))

    # 格式化并输出结果
    print(format_weather_output(all_weather))


if __name__ == "__main__":
    # 示例：查询茂名未来3天天气（默认）
    # 可修改参数测试：例如 main_wttr(city='北京', date_input='2025-11-10', prediction=1)
    main_wttr()