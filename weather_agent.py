import os

import dotenv
import requests
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.tools import Tool
# from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


def get_weather(city):
    """
    获取天气信息
    :param city:
    :return:
    """
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    OPENWEATHER_BASE_URL = os.getenv("OPENWEATHER_BASE_URL")

    params = {
        'appid': OPENWEATHER_API_KEY,
        'q': city,
        'units': 'metric',
        'lang': 'zh_cn',
    }

    response = requests.get(OPENWEATHER_BASE_URL, params=params)

    data = response.json()
    if response.status_code == 200:
        city = data['name']
        country = data['sys']['country']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        description = data['weather'][0]['description']
        feels_like = data['main']['feels_like']

        result = f"🌤️ {city}({country}) 天气信息：\n\n"
        result += f"📊 当前天气：{description}\n"
        result += f"🌡️ 温度：{temp}°C (体感{feels_like}°C)\n"
        result += f"💧 湿度：{humidity}%\n"
        result += f"💨 风速：{wind} m/s\n"

        return result
    else:
        return f"获取天气信息失败：{data.get('message', '未知错误')}"


# weather_tool = Tool(
#     func=get_weather,
#     name="get_weather",
#     description="查询城市天气信息",
# )
#
# llm = ChatOpenAI(model_name="gpt-4o-mini")
#
# prompt_template = ChatPromptTemplate.from_messages([
#     ("system",
#      """你是一个天气查询助手，帮助用户查询城市天气信息。
#
#      重要规则：
#      1. 当用户询问天气时，调用get_weather工具
#      2. 必须将中文城市或者是地区的名称转换为标准的英文名称
#      3. 你只需要输出与天气相关的信息就可以
#
#      转换示例：
#      - "北京" → "Beijing"
#      - "北京市" → "Beijing"
#      - "北京石景山区" → "Beijing"
#      - "上海市" → "Shanghai"
#      - "上海浦东" → "Shanghai"
#      - "广州天河区" → "Guangzhou"
#      - "深圳" → "Shenzhen"
#
#      输入格式必须为：英文城市名称"""),
#     ("human", "{input}"),
#     ("placeholder", "{agent_scratchpad}"),
# ])
#
# agent = create_tool_calling_agent(
#     llm=llm,
#     prompt=prompt_template,
#     tools=[weather_tool],
# )
#
# agent_executor = AgentExecutor(
#     agent=agent,
#     tools=[weather_tool],
#     verbose=True,
#     memory=ConversationBufferMemory()
# )
#
# user_input = input(f"请输入你的问题：")
#
# print(user_input)
# result_weather = agent_executor.invoke({"input": user_input})
# print("\n" + "=" * 50)
# print(result_weather['output'])
# print("=" * 50)
#

