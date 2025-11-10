import requests


def send_to_wechat(send_key, title, desp=''):
    """
    使用Server酱发送消息到微信

    Parameters:
    send_key (str): 你的Server酱SendKey，例如 'SCT302180TUGDW4agBBvoVv5Oa6aOQWD9D'
    title (str): 消息标题，最长为256个字符
    desp (str, optional): 消息内容，支持Markdown格式
    """
    # 构造请求URL
    url = f"https://sctapi.ftqq.com/{send_key}.send"

    # 准备请求数据
    data = {
        "text": title,  # 消息标题
        "desp": desp  # 消息内容（可选）
    }

    try:
        # 发送POST请求[citation:2][citation:8]
        response = requests.post(url, data=data)

        # 检查请求是否成功
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                print("✅ 消息推送成功！")
            else:
                print(f"❌ 推送失败，错误信息：{result.get('message')}")
        else:
            print(f"❌ 请求失败，状态码：{response.status_code}")

    except Exception as e:
        print(f"❌ 发送请求时出现异常：{str(e)}")


# 使用示例 - 请将YOUR_SEND_KEY_HERE替换为你的实际SendKey
if __name__ == "__main__":
    import os
    # 你的SendKey
    my_send_key = SECRET_KEY = os.environ.get('MY_SEND_KEY')

    # 发送一条简单的测试消息
    send_to_wechat(my_send_key, "🚀 来自Python的问候", "你好！这是一条通过Server酱从Python程序发送的测试消息。")

    # 发送带Markdown格式的消息
    markdown_content = """
## 这是一个Markdown格式的消息

- **特点1**：支持粗体、斜体
- **特点2**：支持列表和链接
- **特点3**：支持代码块

`行内代码` 也可以正常显示

[点击访问Server酱官网](https://sct.ftqq.com/)
"""
    send_to_wechat(my_send_key, "📝 Markdown测试", markdown_content)