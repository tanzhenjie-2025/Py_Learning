import random
from typing import List, Dict
import json


def random_joke() -> str:
    """随机笑话插件 - 纯本地版本，不依赖网络"""
    try:
        # 丰富的本地笑话库
        jokes = get_joke_library()
        joke = random.choice(jokes)
        return joke["content"]
    except Exception as e:
        print(f"获取本地笑话失败: {e}")
        return "保持微笑，好运自然来！😊"


def get_joke_library() -> List[Dict]:
    """本地笑话库"""
    return [
        {
            "category": "程序员",
            "content": "为什么程序员总是分不清万圣节和圣诞节？因为 Oct 31 == Dec 25"
        },
        {
            "category": "程序员",
            "content": "程序员最讨厌的购物网站：无码超市"
        },
        {
            "category": "程序员",
            "content": "我：妈，我去写代码了。妈：哦，你注意颈椎啊。我：好。过了会儿，妈：你在写啥代码？我：Python。妈：你写Python的时候，眼镜蛇怎么办？"
        },
        {
            "category": "程序员",
            "content": "问：如何生成一个随机字符串？答：让新手退出vim"
        },
        {
            "category": "程序员",
            "content": "程序员结婚典礼：新郎新娘共同编译爱情程序，结果报错了：Error: 新娘不是静态的(static)"
        },
        {
            "category": "程序员",
            "content": "为什么Java程序员要戴眼镜？因为他们不会C#"
        },
        {
            "category": "程序员",
            "content": "十个0分程序员：一个在写bug，九个在改bug"
        },
        {
            "category": "程序员",
            "content": "程序员解决问题的流程：1. 谷歌 2. 复制 3. 粘贴 4. 运行"
        },
        {
            "category": "程序员",
            "content": "产品经理：这个需求很简单，怎么实现我不管。程序员：..."
        },
        {
            "category": "程序员",
            "content": "测试工程师走进酒吧，要了一杯啤酒，要了一杯咖啡，要了0杯啤酒，要了999999杯啤酒，要了一只蜥蜴..."
        },
        {
            "category": "生活",
            "content": "今天去面试，面试官问我：你有什么特长？我说：我腿特长。面试官：出去！"
        },
        {
            "category": "生活",
            "content": "为什么胖的人更容易快乐？因为心宽体胖嘛！"
        },
        {
            "category": "生活",
            "content": "我问朋友：你怎么天天吃泡面？朋友：我在存钱买房。我：吃泡面能存多少钱？朋友：我买泡面送的房子模型。"
        },
        {
            "category": "生活",
            "content": "今天在电梯里遇到个小朋友，他问我：叔叔，现在几点了？我看着他可爱的脸庞，说：叫哥哥，我就告诉你。小朋友说：哥哥，现在几点了？我说：哥哥也不知道。"
        },
        {
            "category": "动物",
            "content": "为什么鸡要过马路？因为它想去对面的KFC证明自己还没被淘汰。"
        },
        {
            "category": "动物",
            "content": "两只番茄过马路，一辆汽车飞驰而过，其中一只番茄被压扁了。另一只番茄指着被压扁的番茄说：哇，番茄酱！"
        },
        {
            "category": "学习",
            "content": "老师：请用'果然'造句。学生：昨天我先吃苹果然后喝凉水。老师：那是'果然'吗？学生：是呀，我先吃'果'然后喝'水'，不就是'果'然后'水'吗？"
        },
        {
            "category": "学习",
            "content": "数学老师：一座桥承重10吨，一辆卡车重8吨，装了6吨钢卷，问卡车能过桥吗？学生：不能。老师：为什么？学生：卡车司机没吃饭，饿得开不动车。"
        }
    ]


def random_joke_by_category(category: str = None) -> str:
    """按类别获取随机笑话"""
    jokes = get_joke_library()

    if category:
        category_jokes = [joke for joke in jokes if joke["category"] == category]
        if category_jokes:
            return random.choice(category_jokes)["content"]
        else:
            return f"没有找到{category}类别的笑话，来个随机的吧：{random_joke()}"

    return random_joke()


def random_joke_with_format() -> dict:
    """带格式的随机笑话，便于推送"""
    jokes = get_joke_library()
    joke = random.choice(jokes)

    return {
        "type": "joke",
        "title": f"😂 随机笑话 - {joke['category']}",
        "content": joke["content"],
        "category": joke["category"],
        "tip": "开心一笑，放松心情～"
    }


def get_joke_categories() -> List[str]:
    """获取所有笑话分类"""
    jokes = get_joke_library()
    categories = list(set(joke["category"] for joke in jokes))
    return categories


def get_joke_stats() -> dict:
    """获取笑话库统计"""
    jokes = get_joke_library()
    categories = {}

    for joke in jokes:
        category = joke["category"]
        categories[category] = categories.get(category, 0) + 1

    return {
        "total_jokes": len(jokes),
        "categories": categories,
        "categories_count": len(categories)
    }


# 测试函数
def test_joke_plugin():
    """测试笑话插件"""
    print("=== 测试随机笑话 ===")
    print(random_joke())

    print("\n=== 测试程序员笑话 ===")
    print(random_joke_by_category("程序员"))

    print("\n=== 测试带格式笑话 ===")
    formatted_joke = random_joke_with_format()
    print(f"标题: {formatted_joke['title']}")
    print(f"内容: {formatted_joke['content']}")
    print(f"提示: {formatted_joke['tip']}")

    print("\n=== 笑话库统计 ===")
    stats = get_joke_stats()
    print(f"总笑话数: {stats['total_jokes']}")
    print(f"分类数: {stats['categories_count']}")
    print("各分类数量:")
    for category, count in stats['categories'].items():
        print(f"  {category}: {count}个")


# 集成到你的工作流中的示例
def daily_workflow():
    """示例工作流"""
    messages = []

    # 添加笑话
    joke_data = random_joke_with_format()
    messages.append({
        "type": "joke",
        "title": joke_data["title"],
        "content": joke_data["content"]
    })

    # 这里可以添加你的其他功能
    # messages.append(get_weather_forecast())
    # messages.append(get_daily_sentence())

    return messages


if __name__ == "__main__":
    # 运行测试
    test_joke_plugin()

    print("\n" + "=" * 50)
    print("工作流示例输出:")
    workflow_messages = daily_workflow()
    for msg in workflow_messages:
        print(f"[{msg['type']}] {msg['title']}")
        print(f"内容: {msg['content']}")
        print()